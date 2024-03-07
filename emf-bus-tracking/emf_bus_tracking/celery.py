import os
import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emf_bus_tracking.settings')

app = celery.Celery('emf_bus_tracking')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()