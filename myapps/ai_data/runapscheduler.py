# import logging
# from django.conf import settings
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import register_events, DjangoJobStore
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management import BaseCommand

# from models import Count

# logger = logging.getLogger(__name__)

# def question_job():
#     if Count.question_count < 2:
#         Count.question_count = 2
#     else:
#         pass
    
# def answer_job():
#     if Count.answer_count < 1:
#         Count.answer_count = 1
#     else:
#         pass
    
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
        
#         scheduler.add_job(
#             question_job,
#             trigger=CronTrigger(hour="00"),
#             id="question_job",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'question_job'.")
        
#         scheduler.add_job(
#             answer_job,
#             trigger=CronTrigger(hour="00"),
#             id="answer_job",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'answer_job'.")
        
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")