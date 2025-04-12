from celery import Celery
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery