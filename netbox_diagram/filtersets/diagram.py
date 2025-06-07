from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from netbox_diagram.models import Diagram, DiagramAssociation

_all__ = (
    "DiagramFilterSet",
    "DiagramAssociationFilterSet",
)


class DiagramFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Diagram
        fields = (
            "id",
            "name",
            "description",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value)).distinct()


class DiagramAssociationFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = DiagramAssociation
        fields = (
            "id",
            "diagram",
            "assigned_object_type",
            "assigned_object_id",
            "coord_x",
            "coord_y",
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value)).distinct()
