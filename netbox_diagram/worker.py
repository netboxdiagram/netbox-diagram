import logging

from django_rq import job

from netbox_diagram.models import Diagram
from netbox_diagram.utils.diagram import compute_diagram_data

logger = logging.getLogger('worker')


class UpdateDiagramCacheJob:
    def __init__(self, **kwargs):
        self.diagram_id = kwargs.get('diagram_id')

    def run(self):
        try:
            diagram = Diagram.objects.get(pk=self.diagram_id)
            diagram.cached_data = compute_diagram_data(self.diagram_id)
            diagram.save()
        except Diagram.DoesNotExist:
            pass
        except Exception as _err:
            pass


@job('low')
def updatecache(diagram_id):
    worker = UpdateDiagramCacheJob(diagram_id=diagram_id)
    worker.run()
