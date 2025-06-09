# 重启 cellranger 队列
celery multi restart worker -A django_server -l info -f logs/celery_cellranger.log --pidfile=pids/celery_cellranger.pid -n cellranger_worker -Q cellranger
# 重启 默认 队列
celery multi restart worker -A django_server -l info -f logs/celery_default.log --pidfile=pids/celery_default.pid
