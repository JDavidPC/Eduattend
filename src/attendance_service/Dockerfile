# src/attendance_service/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir psycopg2-binary pika

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "-c", "from src.attendance_service.app import create_app; app=create_app(); app.run(host='0.0.0.0', port=8000)"]
