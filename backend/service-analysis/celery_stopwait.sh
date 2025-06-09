# 启动 celery_cellranger 队列
celery multi stopwait worker -A django_server -l info -f logs/celery_cellranger.log --pidfile=pids/celery_cellranger.pid -n cellranger_worker -Q cellranger
# 启动 默认队列
celery multi stopwait worker -A django_server -l info -f logs/celery_default.log --pidfile=pids/celery_default.pid
