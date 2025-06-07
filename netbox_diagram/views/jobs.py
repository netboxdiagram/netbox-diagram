from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django_rq import get_queue

from netbox_diagram.models import Diagram


class TriggerDiagramCacheJobView(View):
    def get(self, request, pk):
        diagram = get_object_or_404(Diagram, pk=pk)
        queue = get_queue('low')
        queue.enqueue_job(
            queue.create_job(
                func='netbox_diagram.worker.updatecache',
                args=[diagram.id],
                timeout=9000,
            )
        )
        messages.success(request, f'Diagram cache update job enqueued for: {diagram.name}')
        return redirect(diagram.get_absolute_url())
