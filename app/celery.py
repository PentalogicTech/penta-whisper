from celery import Celery, Task

celery = Celery("app", broker="redis://127.0.0.1:6379/0", backend = "redis://127.0.0.1:6379/0")

# Configurar opciones de Celery, como imports automáticos de tareas
celery.conf.update(
    task_routes={
        "app.routes.task.process_audio": {"queue": "audio_queue"},
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 30}

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def run (self, *args, **kwargs):
        try:

            pass
        except Exception as e:
            self.retry(exc=e)

celery.autodiscover_tasks([
    'app.routes.task',
])


if __name__ == "__main__":
    celery.start()

