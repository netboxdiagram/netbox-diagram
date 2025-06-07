from dcim.models import Device
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
from utilities.testing import create_test_device

from netbox_diagram.models import Diagram, DiagramAssociation


class DiagramTestCase(TestCase):
    def test_diagram_creation(self):
        diagram = Diagram(name='Demo', description='Demo Description')
        diagram.full_clean()
        diagram.save()

    def test_diagram_unique_name_constraint(self):
        Diagram.objects.create(name='UniqueName')
        with self.assertRaises(Exception):
            Diagram.objects.create(name='UniqueName')

    def test_diagram_creation_without_name(self):
        diagram = Diagram(description='Demo Description')
        with self.assertRaises(ValidationError):
            diagram.full_clean()
        diagram.save()

    def test_diagram_creation_without_name(self):
        diagram = Diagram(description='Demo Description')
        with self.assertRaises(ValidationError):
            diagram.full_clean()
        diagram.save()


class DiagramAssociationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        diagrams = (Diagram(name='Diagram 1'),)
        Diagram.objects.bulk_create(diagrams)

    def test_diagramassociation_creation(self):
        device = create_test_device(name='Device 1')
        device_ct = ContentType.objects.get_for_model(Device)

        diagramassociation = DiagramAssociation(diagram=Diagram.objects.first(), assigned_object_type=device_ct, assigned_object_id=device.id)
        diagramassociation.full_clean()
        diagramassociation.save()

    def test_diagramassociation_creation_with_multiple_devices(self):
        device_1 = create_test_device(name='Device 1')
        device_2 = create_test_device(name='Device 2')

        device_ct = ContentType.objects.get_for_model(Device)

        diagramassociation_1 = DiagramAssociation(diagram=Diagram.objects.first(), assigned_object_type=device_ct, assigned_object_id=device_1.id)
        diagramassociation_1.full_clean()
        diagramassociation_1.save()

        diagramassociation_2 = DiagramAssociation(diagram=Diagram.objects.first(), assigned_object_type=device_ct, assigned_object_id=device_2.id)
        diagramassociation_2.full_clean()
        diagramassociation_2.save()
