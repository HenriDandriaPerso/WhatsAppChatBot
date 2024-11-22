import os

_port = os.environ.get("PORT", 5006)
bind = [f"[::]:{_port}"]

# Use the Uvicorn worker class suited for FastAPI (ASGI applications)
worker_class = "uvicorn.workers.UvicornWorker"

workers = int(os.environ.get("WEB_CONCURRENCY", 1))
threads = int(os.environ.get("GUNICORN_THREADS", 5))

preload_app = True

# Adjust the timeout settings as needed
timeout = 20
graceful_timeout = 20

# Additional Gunicorn settings (optional)
keepalive = 5
errorlog = "-"
accesslog = "-"
loglevel = "info"
