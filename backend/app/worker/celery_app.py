"""
Celery application configuration.

This module sets up a Celery instance that the FastAPI app and
background workers can share.  The broker and result backend are
configured to use Redis, which is provided as a separate service
via docker-compose.  The ``task_track_started`` flag enables
progress reporting for long‑running tasks.
"""

from celery import Celery


# Create the Celery application.  The name "tasks" identifies
# the module to Celery and will be used when registering tasks.
celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

# Enable tracking when a task starts.  Without this setting the
# ``task_state`` attribute would go directly from ``PENDING`` to
# ``SUCCESS`` without intermediate progress updates.
celery.conf.update(task_track_started=True)