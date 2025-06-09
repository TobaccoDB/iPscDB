#!/bin/bash

# 应用数据库迁移
python manage.py makemigrations
python manage.py migrate

# 启动Gunicorn (后台运行)
gunicorn your_project_name.wsgi:application --bind 0.0.0.0:8002 &

# 启动Celery (根据实际需要)
sh celery_start.sh

# 保持容器运行
tail -f /dev/null
