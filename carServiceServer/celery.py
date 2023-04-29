import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carServiceServer.settings")
app = Celery("carServiceServer")

from carService.tasks import send_best_district

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, send_best_district.s(), name='send_best_district every 10')


@app.task
def test(arg):
    print(arg)
