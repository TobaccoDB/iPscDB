import os
from kombu import Queue, Exchange

SECRET_KEY = 'django-insecure-u^y)js2e-y4j1&^^2d)z)$fhe^uigq^0s@hi=!0=bt3=-=u@wk'
# ======================
# = Databases Settings
# ======================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'NAME': os.environ.get('DB_ANALYSIS_NAME'),
        'HOST': 'db',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'
        }
    }
}


# ======================
# = Celery Settings ====
# ======================

# rabbitmq 做消息中间件，配置规则'amqp://用户名:密码@rabbitmq服务器地址:5672'
CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672'
# redis 做消息中间件
# CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
# celery运行结果存储方式，可以是django-db中，也可以是存放在redis中，比如（redis://127.0.0.1:6379/2）。
# 支持数据库django-db和缓存django-cache存储任务状态及结果，建议选django-db
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'django-db'
# 设置celery头信息中，接受的数据格式，要与其他两个参数想对应(默认是json格式)
# CELERY_ACCEPT_CONTENT
CELERY_TIMEZONE = 'Asia/Shanghai'

# 配置队列
CELERY_QUEUES = (
    Queue('default', exchange=Exchange('default'), routing_key='default'),
    Queue('cellranger', exchange=Exchange('cellranger'), routing_key='cellranger'),  # consumer_arguments={'x-priority': 10}),
)

# 防止队列重启导致任务失败
# 任务失败或超时自动确认，默认为True
# CELERY_ACKS_ON_FAILURE_OR_TIMEOUT=False
# 任务完成之后再确认
CELERY_ACKS_LATE=True
# worker进程崩掉之后拒绝确认
CELERY_REJECT_ON_WORKER_LOST=True

# 防止内存泄漏
# CELERYD_CONCURRENCY = 10  # celery worker 的并发数
# CELERYD_PREFETCH_MULTIPLIER = 6  # celery worker 每次去BROKER中预取任务的数量
# CELERYD_MAX_TASKS_PER_CHILD = 10  # 每个worker最大执行任务数
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁

CELERY_IGNORE_RESULT = False
CELERY_TASK_TRACK_STARTED = True
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


DJANGO_CELERY_BEAT_TZ_AWARE = False
# 使用django_celery_beat插件用来动态配置任务！
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# ======================
# = Analyse Settings ====
# ======================

ANALYSE_BASE_DIR = "/data/Data_analyse"
TRANSCRIPTOME_BASE_DIR = "/data/Data_analyse"

#下载时候的IP拼接
ANALYSIS_BASE_URL=f'{os.environ.get('ANALYSIS_BASE_URL')}/'