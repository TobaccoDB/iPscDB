import json

from django_celery_beat.models import CrontabSchedule, IntervalSchedule, ClockedSchedule, PeriodicTask
from django.core.management.base import BaseCommand

 
class Command(BaseCommand):

    def handle(self, *args, **options):
        # 创建定时任务
        interval_schedule, _ = IntervalSchedule.objects.update_or_create(
            every=1, 
            period=IntervalSchedule.MINUTES
        )   # 按分钟间隔执行 
        PeriodicTask.objects.update_or_create(
            defaults= {
                "interval": interval_schedule,
                "task": "mul_num",
                "kwargs": json.dumps({"x": 8, "y": 9}, ensure_ascii=False)
            },
            name= "定时interval-task-1"
        )