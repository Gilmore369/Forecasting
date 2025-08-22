"""
Celery tasks for model training and evaluation.

This module defines the background task that iterates over all
available forecasting models, trains each on a given time series,
computes metrics and returns the results ordered by MAPE.  Progress
is reported back to the caller via Celery's state mechanism.
"""

from __future__ import annotations

from typing import List, Dict, Any

import time
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error

from .celery_app import celery


# Placeholder registry of all available models.  In a full
# implementation you would import concrete model classes and store
# them here keyed by user‑friendly names.  See the commented
# imports below for an example of how this might look.
# from app.models.traditional import SimpleMovingAverageModel
# from app.models.arima import AutoArimaModel
ALL_MODELS: Dict[str, Any] = {
    # "Simple Moving Average": SimpleMovingAverageModel,
    # "AutoARIMA": AutoArimaModel,
    # Add additional models here...
}


@celery.task(bind=True)
def run_all_models_task(self, data: List[float]) -> Dict[str, Any]:
    """Evaluate a suite of forecasting models on the provided data.

    The task iterates through a preconfigured list of models,
    training each one and computing error metrics.  While running it
    updates its state to communicate progress back to the caller.
    Currently this function simulates work using dummy data.

    :param self: The bound Celery task instance used for updating
        state.  Celery binds ``self`` when ``bind=True`` is set.
    :param data: The time series data to train models on
    :returns: A dictionary with overall status and a list of results
    """
    series = pd.Series(data, dtype=float)
    results: List[Dict[str, Any]] = []
    # For demonstration we define a small list of placeholder model
    # names.  In a real system you would iterate over ALL_MODELS.
    dummy_models = [
        "Media Móvil Simple",
        "Suavizado Exponencial",
        "ARIMA",
        "Prophet",
        "Random Forest",
    ]
    total_models = len(dummy_models)

    for i, model_name in enumerate(dummy_models):
        # Update the task state to report progress.  The ``meta``
        # dictionary can include any additional information, such as
        # the current model name and the number processed so far.
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': total_models,
                'model': model_name,
            },
        )
        # Simulate model training time.  Replace this with real
        # training and evaluation code.  Sleep for a short period to
        # make progress visible when polling.
        time.sleep(2)
        # In a full implementation you would instantiate the model,
        # split ``series`` into training and validation sets,
        # compute predictions, then calculate metrics.  Here we
        # fabricate deterministic metrics for demonstration.
        results.append({
            "model_name": model_name,
            "metrics": {
                "mape": 10.5 + i * 0.8,
                "mae": 100.2 + i * 1.3,
                "mse": 15000.1 + i * 100.0,
                "rmse": 122.5 + i * 0.9,
            },
            "params": "{'n': 3}",
        })
    # Sort the results by ascending MAPE so the best performer appears first
    results.sort(key=lambda x: x['metrics']['mape'])
    return {
        "status": "SUCCESS",
        "results": results,
    }