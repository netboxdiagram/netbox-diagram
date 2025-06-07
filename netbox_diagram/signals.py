from circuits.models import CircuitTermination
from dcim.models import Cable
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_rq import get_queue

from netbox_diagram.models import DiagramAssociation
from netbox_diagram.utils.diagram import compute_diagram_data


@receiver([post_save, post_delete], sender=DiagramAssociation)
def update_diagram_on_association_change(sender, instance, **kwargs):
    if instance.diagram:
        queue = get_queue("low")
        queue.enqueue_job(
            queue.create_job(
                func="netbox_diagram.worker.updatecache",
                args=[instance.diagram.id],
                timeout=9000,
            )
        )


@receiver([post_save, post_delete], sender=Cable)
def update_diagram_on_cable_change(sender, instance, **kwargs):
    termination_ids = []
    content_types = []

    for t in instance.terminations.all():
        term = getattr(t, "termination", None)
        if term:
            termination_ids.append(term.id)
            content_types.append(ContentType.objects.get_for_model(term))

    filters = Q()
    for ct, id_ in zip(content_types, termination_ids):
        filters |= Q(assigned_object_type=ct, assigned_object_id=id_)

    diagram_ids = DiagramAssociation.objects.filter(filters).values_list("diagram_id", flat=True).distinct()
    for diagram_id in diagram_ids:
        queue = get_queue("low")
        queue.enqueue_job(
            queue.create_job(
                func="netbox_diagram.worker.updatecache",
                args=[diagram_id],
                timeout=9000,
            )
        )


@receiver([post_save, post_delete], sender=CircuitTermination)
def update_diagram_on_circuit_termination_change(sender, instance, **kwargs):
    assigned_object = getattr(instance.termination, "device", None)
    if assigned_object:
        associations = DiagramAssociation.objects.filter(
            assigned_object_id=assigned_object.id,
            assigned_object_type=ContentType.objects.get_for_model(assigned_object),
        )
        for assoc in associations:
            assoc.diagram.cached_data = compute_diagram_data(assoc.diagram.id)
            assoc.diagram.save()
