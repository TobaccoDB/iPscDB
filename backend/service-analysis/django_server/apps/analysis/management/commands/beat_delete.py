import json

from django_celery_beat.models import CrontabSchedule, IntervalSchedule, ClockedSchedule, PeriodicTask
from django_celery_beat.schedulers import DatabaseScheduler
from django.core.management.base import BaseCommand

from django_server.celery import app
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        # 删除的指定的任务
        periodic_task = PeriodicTask.objects.get(name='定时interval-task-1')
        periodic_task.delete()
        # 重启一下定时任务
        scheduler = DatabaseScheduler(app)
        scheduler.sync()
        