from __future__ import absolute_import, unicode_literals
import os
from logging.config import dictConfig

from django.conf import settings
from celery import Celery
from celery.signals import setup_logging

""" RabbitMQ as message broker
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'AIC21_Backend.settings.production')
app = Celery(main='AIC21_Backend',
             broker='amqp://aic:shitWasHereBe4me@rabbitmq:5672')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
