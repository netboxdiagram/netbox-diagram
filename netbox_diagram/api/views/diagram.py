from netbox.api.viewsets import NetBoxModelViewSet

from netbox_diagram.api.serializers import DiagramAssociationSerializer, DiagramSerializer
from netbox_diagram.filtersets import DiagramAssociationFilterSet, DiagramFilterSet
from netbox_diagram.models import Diagram, DiagramAssociation

__all__ = (
    'DiagramViewSet',
    'DiagramAssociationViewSet',
)


class DiagramViewSet(NetBoxModelViewSet):
    queryset = Diagram.objects.all()
    serializer_class = DiagramSerializer
    filterset_class = DiagramFilterSet


class DiagramAssociationViewSet(NetBoxModelViewSet):
    queryset = DiagramAssociation.objects.all()
    serializer_class = DiagramAssociationSerializer
    filterset_class = DiagramAssociationFilterSet
