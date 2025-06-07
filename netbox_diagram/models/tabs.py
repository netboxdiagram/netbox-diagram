from circuits.models import Circuit
from dcim.models import Device
from django.contrib.contenttypes.models import ContentType

from .diagram import DiagramAssociation


# Monkeypatch
def get_diagram_associations(obj):
    associations = []
    for association in DiagramAssociation.objects.filter(
        assigned_object_type=ContentType.objects.get_for_model(obj),
        assigned_object_id=obj.id,
    ):
        associations.append(association)

    return associations


setattr(Device, 'get_diagram_associations', get_diagram_associations)
setattr(Circuit, 'get_diagram_associations', get_diagram_associations)
