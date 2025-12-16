from app.worker.celery_app import celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery_app.task(ack_late=True)
def test_celery(word: str) -> str:
    logger.info(f"Test task received: {word}")
    return f"test task return {word}"
