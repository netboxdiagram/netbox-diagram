from django.test import TestCase

from dcim.models import Device, Manufacturer
from circuits.models import Circuit, CircuitTermination, CircuitType, Provider

from utilities.testing import create_test_device

from netbox_diagram.forms import *
from netbox_diagram.models import *


class DiagramTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_valid_diagram(self):
        form = DiagramForm(data={
            'name': 'DiagramForm 1',
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_invalid_form_missing_name(self):
        form = DiagramForm(data={"description": "Test without name"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class DiagramAssociationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Diagram.objects.create(name='DiagramForm 2')

    def test_device_assignment(self):
        device = create_test_device(name='Device')

        form = DiagramAssociationForm(data={
            'diagram': Diagram.objects.first(),
            'device': device.id
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_circuit_assignment(self):
        provider = Provider.objects.create(name="Provider 1", slug="provider-1")
        circuittype = CircuitType.objects.create(name="Circuit Type 1", slug="circuit-type-1")
        circuit = Circuit.objects.create(provider=provider, type=circuittype, cid="1")

        form = DiagramAssociationForm(data={
            'diagram': Diagram.objects.first(),
            'circuit': circuit.id
        })
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_assignment_without_object(self):
        form = DiagramAssociationForm(data={
            'diagram': Diagram.objects.first(),
        })
        self.assertFalse(form.is_valid())

    def test_circuit_assignment_without_diagram(self):
        provider = Provider.objects.create(name="Provider 1", slug="provider-1")
        circuittype = CircuitType.objects.create(name="Circuit Type 1", slug="circuit-type-1")
        circuit = Circuit.objects.create(provider=provider, type=circuittype, cid="1")

        form = DiagramAssociationForm(data={
            'circuit': circuit.id
        })
        self.assertFalse(form.is_valid())

    def test_device_assignment_without_diagram(self):
        device = create_test_device(name='Device')

        form = DiagramAssociationForm(data={
            'device': device.id
        })
        self.assertFalse(form.is_valid())
