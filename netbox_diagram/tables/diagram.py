import django_tables2 as tables
from netbox.tables import NetBoxTable

from netbox_diagram.models import Diagram, DiagramAssociation

_all__ = (
    "DiagramTable",
    "DiagramAssociationTable",
)


class DiagramTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Diagram
        fields = (
            "pk",
            "name",
            "description",
            "created",
            "last_updated",
        )
        default_columns = (
            "pk",
            "name",
            "description",
        )


class DiagramAssociationTable(NetBoxTable):
    diagram = tables.Column(linkify=True)
    assigned_object = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = DiagramAssociation
        fields = (
            "pk",
            "diagram",
            "assigned_object_type",
            "assigned_object",
            "coord_x",
            "coord_y",
            "created",
            "last_updated",
        )
        default_columns = (
            "pk",
            "diagram",
            "assigned_object_type",
            "assigned_object",
            "description",
        )
