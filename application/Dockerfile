FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/

RUN pip install --no-cache-dir pytz

CMD ["python", "app.py"]
