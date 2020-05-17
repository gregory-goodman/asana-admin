import asana
from django.conf import settings


class Asana:
    def _client(self):
        return asana.Client.access_token(settings.PERSONAL_ACCESS_TOKEN)

    def get_workspace(self):
        return self._client().users.me()['workspaces'][0]['gid']

    def get_project_by_id(self, project_id):
        return self._client().projects.find_by_id(project_id)

    def create_project(self, title):
        return self._client().projects.create_in_workspace(self.get_workspace(), {'name': title})

    def update_project(self, project_id, title):
        return self._client().projects.update(project_id, {'name': title})

    def get_all_projects(self):
        return list(self._client().projects.find_all({'workspace': self.get_workspace()}))

    def create_task(self, projects_ids, title, executor_id=None, description=None):
        print(executor_id)
        print(            {
                'project': projects_ids,
                'name': title,
                'assignee': executor_id,
                'notes': description
             })
        return self._client().tasks.create_in_workspace(
            self.get_workspace(),
            {
                'projects': projects_ids,
                'name': title,
                'assignee': executor_id,
                'notes': description
             }
        )

    def update_task(self, task_id, title, executor_id=None, description=None):
        return self._client().tasks.update(
            task_id,
            {
                'name': title,
                'assignee': executor_id,
                'notes': description
             }
        )

    def get_tasks_by_project(self, project_id):
        return list(self._client().tasks.find_all({'project': project_id}))

    def get_task_by_id(self, task_id):
        return self._client().tasks.find_by_id(task_id)

    def get_all_users(self):
        return list(self._client().users.find_all({'workspace': self.get_workspace()}))
