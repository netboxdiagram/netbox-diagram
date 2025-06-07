import json

from circuits.models import Circuit
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.generic import View

from netbox_diagram.models import Diagram, DiagramAssociation


class DiagramData(View):
    def get(self, request, *args, **kwargs):
        diagram_id = kwargs.get('pk')
        diagram = Diagram.objects.get(pk=diagram_id)
        return JsonResponse(diagram.cached_data or {})

    def post(self, request, *args, **kwargs):
        try:
            diagram_id = kwargs.get('pk', None)
            data = json.loads(request.body)

            for node in data:
                # If no association_id, the node has been automatically added to ensure the diagram is correct
                if not node['association_id']:
                    # Circuit logic
                    if node['type'] == 'circuit':
                        circuit_obj = Circuit.objects.get(cid=node['name'])
                        # Circuit cannot be found on the name, thats odd...
                        if not circuit_obj:
                            continue

                        # Create the association
                        obj_type = ContentType.objects.get_for_model(circuit_obj)
                        diagram_association = DiagramAssociation.objects.create(
                            diagram_id=diagram_id,
                            assigned_object_type=obj_type,
                            assigned_object_id=circuit_obj.id,
                            coord_x=node['x'],
                            coord_y=node['y'],
                        )
                        node['association_id'] = diagram_association.id

                diagramassociation = DiagramAssociation.objects.get(id=node['association_id'])

                updated = False

                if diagramassociation.coord_x != node['x']:
                    diagramassociation.coord_x = node['x']
                    updated = True

                if diagramassociation.coord_y != node['y']:
                    diagramassociation.coord_y = node['y']
                    updated = True

                if updated:
                    diagramassociation.save()

            return JsonResponse({'status': 'success', 'message': 'Positions saved.'})
        except Exception as _err:
            print(_err)
            return JsonResponse({'status': 'error', 'message': str(_err)}, status=400)
