"""
Main entry point for the ForecastForge backend.

This file initialises the FastAPI application, configures CORS to
allow the front‑end to communicate with the API and mounts the
router defined in ``app/api/endpoints.py`` under the ``/api``
prefix.  When run under uvicorn the application exposes a simple
root endpoint for basic health checking.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router


# Create the FastAPI application with a descriptive title.  The
# backend will serve requests made by the React front‑end.
app = FastAPI(title="ForecastForge API")

# Allow the React front‑end running on localhost:3000 to make
# cross‑origin requests to the API.  Without this configuration
# the browser would block requests due to CORS policy.  The
# settings below grant all methods and headers, which is
# appropriate for a development environment.  In production you
# should restrict the allowed origins to your deployed front‑end.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    """Health check endpoint.

    Returns a simple welcome message indicating that the API is
    running.  Clients may use this endpoint to verify the server
    is reachable.
    """
    return {"message": "Welcome to the ForecastForge API"}


# Mount the API router so that all of the endpoints under
# ``app/api/endpoints.py`` are available at ``/api``.  See
# ``app/api/endpoints.py`` for the actual route implementations.
app.include_router(api_router, prefix="/api")