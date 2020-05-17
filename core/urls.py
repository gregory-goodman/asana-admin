from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'task-board/', include('task_board.urls'), name='task_board'),

]

admin.site.index_template = 'admin/index.html'
admin.autodiscover()
