from django.urls import path, include

from task_board.views import SynchronizationTaskBoard

app_name = 'task_board'

urlpatterns = [
    path(r'synchronization/', SynchronizationTaskBoard.as_view(), name='synchronization'),
]
