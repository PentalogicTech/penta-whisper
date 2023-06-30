from celery import Celery

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

celery.autodiscover_tasks([
    'app.routes.task',
])


if __name__ == "__main__":
    celery.start()

