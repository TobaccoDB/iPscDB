FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8002
# CMD ["gunicorn", "--bind", "0.0.0.0:8001", "service-api.wsgi:application"]
# CMD ["bash", "-c", "python manage.py makemigrations&& python manage.py migrate && gunicorn your_django_project.wsgi:application --bind 0.0.0.0:8002"]
# CMD ["bash", "-c", "sh celery_start.sh"]
RUN chmod +x /start.sh
RUN chmod +x /celery_start.sh
ENTRYPOINT ["/entrypoint.sh"]