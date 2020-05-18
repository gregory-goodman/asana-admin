from django.contrib import admin

from task_board.models import Project, Executor, Task


class TaskAdminInline(admin.TabularInline):
    model = Task
    readonly_fields = ('asana_id',)
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (TaskAdminInline,)
    list_display = ('title', 'asana_id')
    readonly_fields = ('asana_id',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'executor', 'asana_id')
    readonly_fields = ('asana_id',)


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    inlines = (TaskAdminInline,)
    list_display = ('name', 'asana_id')
    readonly_fields = ('asana_id',)

