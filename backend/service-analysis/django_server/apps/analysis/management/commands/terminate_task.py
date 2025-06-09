from celery.control import inspect, terminate
from django_server.celery import app
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        # 删除的指定的任务
        task_id = 'c7cb6cae-1744-44da-8c5d-4083adaffef6'
        terminate.terminate(task_id, destination=[])
