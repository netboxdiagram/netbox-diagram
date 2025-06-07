from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField, Q
from netbox.models import NetBoxModel

_all__ = (
    "Diagram",
    "DiagramAssociation",
)


class Diagram(NetBoxModel):
    name = models.CharField(blank=False)
    description = models.CharField(blank=True)
    cached_data = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Diagram"
        verbose_name_plural = "Diagrams"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="%(app_label)s_%(class)s_unique__name",
                violation_error_message="The diagram name must be unique",
            )
        ]

    def __str__(self):
        return self.name


class DiagramAssociation(NetBoxModel):
    diagram = models.ForeignKey(
        to="netbox_diagram.Diagram",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=Q(
            Q(app_label="dcim", model="device")
            | Q(app_label="circuits", model="circuit")
            | Q(app_label="netbox_diagram", model="DiagramAssociation")
        ),
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
    )
    assigned_object_id = models.PositiveBigIntegerField(blank=True, null=True)
    assigned_object = GenericForeignKey(ct_field="assigned_object_type", fk_field="assigned_object_id")
    coord_x = models.IntegerField(default=20)
    coord_y = models.IntegerField(default=20)

    class Meta:
        verbose_name = "Diagram Association"
        verbose_name_plural = "Diagram Assocations"

        constraints = [
            models.UniqueConstraint(
                fields=["diagram", "assigned_object_type", "assigned_object_id"],
                name="%(app_label)s_%(class)s_unique_object_diagram_name",
                violation_error_message="An object can only be associated to a diagram once",
            )
        ]

    def clean(self):
        super().clean()
        if self.assigned_object_type is None or self.assigned_object_id is None:
            raise ValidationError("An assigned object must be provided")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        ret_val = ""
        if self.assigned_object:
            ret_val = str(self.assigned_object)
        if self.diagram:
            ret_val = f"{ret_val} - {self.diagram.name}"

        return ret_val
