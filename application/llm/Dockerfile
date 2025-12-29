FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY log_analyzer.py .
COPY llm_processor.py .
COPY log_memory.py .
COPY email_notification.py .

# Expose the port matching your internal Vector sink configuration
EXPOSE 8081

# Run the application using Gunicorn for production robustness
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "log_analyzer:app", "--bind", "0.0.0.0:8081",  "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info"]

