from task_board.asana import Asana
from task_board.models import Project, Task, Executor
from task_board.utils import get_object_or_None


def sync_asana_data():
    asana_executor_list = Asana().get_all_users()
    for asana_executor in asana_executor_list:
        name = asana_executor['name']
        executor, exists = Executor.objects.get_or_create(
            asana_id=asana_executor['gid'],
        )
        executor.name = name
        executor.save()
    asana_project_list = Asana().get_all_projects()
    for asana_project in asana_project_list:
        asana_project_id = asana_project['gid']
        title = asana_project['name']
        project, exists = Project.objects.get_or_create(
            asana_id=asana_project_id,
        )
        project.title = title
        project.save()
        asana_tasks_in_project = Asana().get_tasks_by_project(project_id=asana_project_id)
        for asana_task in asana_tasks_in_project:
            asana_task_id = asana_task['gid']
            detailed_task = Asana().get_task_by_id(task_id=asana_task_id)
            asana_executor = detailed_task.get('assignee')
            title = detailed_task['name']
            description = detailed_task['notes']
            executor = None
            if asana_executor:
                executor = get_object_or_None(Executor, asana_id=asana_executor['gid'])
            task = get_object_or_None(Task, asana_id=asana_task_id)
            if not task:
                Task.objects.create(
                    asana_id=asana_task_id,
                    title=title,
                    description=description,
                    project=project,
                    executor=executor
                )
            else:
                task.title = detailed_task['name']
                task.description = detailed_task['notes']
                task.project = project
                task.executor = executor
                task.save()
