import os
from app import mongo
from app.services.elasticsearch_service import es_service
from celery import Celery

celery = Celery(
    'app',
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

@celery.task
def index_plan_task(plan_id, plan_data):
    """Index a plan in Elasticsearch asynchronously"""
    if plan_data:
        es_service.index_plan(plan_data)
    return {"status": "Plan indexed", "plan_id": plan_id}

@celery.task
def update_plan_task(plan_id, plan_data):
    """Update a plan in Elasticsearch asynchronously"""
    if plan_data:
        es_service.update_plan(plan_id, plan_data)
    return {"status": "Plan updated in index", "plan_id": plan_id}

@celery.task
def delete_plan_task(plan_id):
    """Delete a plan from Elasticsearch asynchronously"""
    es_service.delete_plan(plan_id)
    return {"status": "Plan deleted from index", "plan_id": plan_id}