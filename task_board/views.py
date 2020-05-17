from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from task_board.tasks import asana_synchronization_task


@method_decorator(staff_member_required, name='dispatch')
class SynchronizationTaskBoard(View):

    def get(self, request):
        asana_synchronization_task.delay()
        return redirect(reverse('admin:index'))
