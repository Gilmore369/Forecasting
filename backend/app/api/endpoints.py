"""
HTTP API endpoints for ForecastForge.

This module defines the routes exposed by the FastAPI application.  It
provides endpoints for initiating the model evaluation process
(``/process``), checking the status of an evaluation task
(``/results/{task_id}``), and re‑training a selected model to
generate future forecasts (``/forecast``).  The actual heavy
computation runs in Celery workers defined in ``app/worker/tasks.py``.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from celery.result import AsyncResult
import pandas as pd
import io

from app.worker.tasks import run_all_models_task

router = APIRouter()


@router.post("/process")
async def process_data(file: UploadFile = File(...)) -> dict[str, str]:
    """Accept a CSV file containing a 'demanda' column and enqueue the
    model evaluation task.

    This endpoint validates the uploaded file to ensure it is a CSV
    containing a ``demanda`` column with between 12 and 120
    observations.  If validation passes a Celery task is queued
    asynchronously.  The caller receives a ``task_id`` which can be
    polled using ``/results/{task_id}``.

    :param file: Uploaded CSV file
    :raises HTTPException: if the file format or contents are invalid
    :return: JSON containing the Celery task ID
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV.")
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
        if 'demanda' not in df.columns:
            raise HTTPException(status_code=400, detail="El CSV debe tener una columna 'demanda'.")
        data = df['demanda'].dropna().tolist()
        if not (12 <= len(data) <= 120):
            raise HTTPException(status_code=400, detail="La serie debe tener entre 12 y 120 valores.")
        # Enqueue the Celery task; Celery returns an AsyncResult which
        # contains the task ID.  The computation happens in a
        # background worker and will not block this request.
        task = run_all_models_task.delay(data)
        return {"task_id": task.id}
    except HTTPException:
        # Reraise explicit HTTP errors so FastAPI handles them
        raise
    except Exception as exc:
        # Unexpected errors are converted into a generic 500 response
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {exc}")


@router.get("/results/{task_id}")
async def get_results(task_id: str) -> dict:
    """Return the current status or result for a Celery evaluation task.

    When called with a ``task_id`` this endpoint inspects the status
    of the corresponding Celery task.  If the task has finished
    executing the full result is returned.  Otherwise the status
    (``PENDING``, ``PROGRESS``) and any progress metadata are
    returned.  The front‑end is expected to poll this endpoint until
    the task completes.

    :param task_id: The Celery task ID to look up
    :return: JSON describing the task status and metadata or result
    """
    task_result = AsyncResult(task_id)
    if task_result.ready():
        # Task finished; return the result dictionary
        return task_result.get()
    # Task still running or pending; return status and meta
    return {"status": task_result.state, "meta": task_result.info or {}}


@router.post("/forecast")
async def forecast(model_name: str, file: UploadFile = File(...)) -> dict:
    """Train a single model on the full dataset and return a 12‑month forecast.

    The front‑end can call this endpoint once a model has been
    selected.  It retrains the specified model on all available
    historical data and computes a forecast for the next twelve
    periods.  For demonstration purposes this implementation returns a
    dummy forecast.  In a full implementation you would locate the
    model class in your catalogue (see ``app/worker/tasks.ALL_MODELS``)
    and call its predict method.

    :param model_name: The name of the model to train
    :param file: CSV file containing the original ``demanda`` column
    :return: Predicted values and confidence intervals
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV.")
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
        if 'demanda' not in df.columns:
            raise HTTPException(status_code=400, detail="El CSV debe tener una columna 'demanda'.")
        series = df['demanda'].dropna().astype(float)
        # In a real implementation you would retrieve the model
        # corresponding to ``model_name`` from ALL_MODELS, fit it on
        # ``series`` and compute the forecast.  Here we return a
        # dummy increasing sequence to illustrate the response
        # structure.  Each forecast entry has a predicted value and
        # arbitrary confidence interval bounds.
        forecast_horizon = 12
        last_value = series.iloc[-1] if not series.empty else 0.0
        predictions = []
        for i in range(1, forecast_horizon + 1):
            base = last_value * (1 + 0.05 * i)
            predictions.append({
                "period": i,
                "prediction": base,
                "lower_bound": base * 0.95,
                "upper_bound": base * 1.05,
            })
        return {
            "model_name": model_name,
            "forecast": predictions,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error durante el pronóstico: {exc}")