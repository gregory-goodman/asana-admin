from asana.error import NotFoundError, InvalidRequestError

from core.celery import celery_app
from task_board.asana import Asana
from task_board.helpers import sync_asana_data
from task_board.models import Project, Task
from task_board.utils import get_object_or_None


@celery_app.task
def asana_synchronization_task():
    sync_asana_data()


@celery_app.task
def update_or_create_project(project_id):
    project = get_object_or_None(Project, id=project_id)
    if not project:
        return
    asana_project = Asana().get_project_by_id(project.asana_id)
    if isinstance(asana_project, list):
        asana_project = Asana().create_project(title=project.title)
    else:
        asana_project = Asana().update_project(project.asana_id, project.title)
    Project.objects.filter(id=project_id).update(asana_id=asana_project['gid'])


@celery_app.task
def update_or_create_task(task_id):
    task = get_object_or_None(Task, id=task_id)
    if not task:
        return
    executor_id = task.executor.asana_id if task.executor else None
    try:
        asana_task = Asana().get_task_by_id(task.asana_id)
    except (NotFoundError, InvalidRequestError):
        asana_task = Asana().create_task(
            projects_ids=[task.project.asana_id],
            title=task.title,
            description=task.description,
            executor_id=executor_id
        )
    else:
        asana_task = Asana().update_task(
            task_id=task.asana_id,
            title=task.title,
            description=task.description,
            executor_id=executor_id
        )
    Task.objects.filter(id=task_id).update(asana_id=asana_task['gid'])

