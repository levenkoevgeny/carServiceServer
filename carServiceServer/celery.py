import os

from celery import Celery
from carService.tasks import say_hello

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')

app = Celery('Server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(1, say_hello.s(), name='add every 10')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3, say_hello.s(), name='add every 10')


@app.task
def test(arg):
    print(arg)