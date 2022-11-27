#https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from groups.models import Party
from groups.email_pairings import Emailer
import logging

def start():
    scheduler = BackgroundScheduler()
    emailer = Emailer()
    scheduler.add_job(emailer.email_pairings, 'interval', days=1)
    scheduler.start()