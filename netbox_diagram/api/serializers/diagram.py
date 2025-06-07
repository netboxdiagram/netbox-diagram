from django.contrib.contenttypes.models import ContentType
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers
from utilities.api import get_serializer_for_model

from netbox_diagram.models import Diagram, DiagramAssociation

__all__ = (
    "DiagramSerializer",
    "DiagramAssociationSerializer",
)


class DiagramSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_diagram-api:diagram-detail")

    class Meta:
        model = Diagram
        fields = (
            "url",
            "id",
            "display",
            "name",
            "description",
        )


class DiagramAssociationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_diagram-api:diagramassociation-detail")
    # diagram = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_diagram-api:diagram-detail")
    assigned_object_type = ContentTypeField(queryset=ContentType.objects.all())
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DiagramAssociation
        fields = (
            "url",
            "id",
            "display",
            "diagram",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "coord_x",
            "coord_y",
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_assigned_object(self, instance):
        if not instance.assigned_object_type:
            return {}

        serializer = get_serializer_for_model(instance.assigned_object_type.model_class())
        context = {"request": self.context["request"]}
        return serializer(instance.assigned_object, context=context).data
