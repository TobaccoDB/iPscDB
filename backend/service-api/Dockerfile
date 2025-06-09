FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
# CMD ["gunicorn", "--bind", "0.0.0.0:8001", "service-api.wsgi:application"]
CMD ["bash", "-c", "python manage.py makemigrations&& python manage.py migrate && gunicorn your_django_project.wsgi:application --bind 0.0.0.0:8001"]