from django.test import TestCase

from dcim.models import Manufacturer, Device, DeviceType, ModuleType
from utilities.testing import create_test_device

from netbox_diagram.filtersets import *
from netbox_diagram.models import *


class DiagramTestCase(TestCase):
    queryset = Diagram.objects.all()
    filterset = DiagramFilterSet

    @classmethod
    def setUpTestData(cls):
        diagrams = (
            Diagram(name="Diagram 1"),
            Diagram(name="Diagram 2"),
            Diagram(name="Diagram 3"),
        )
        Diagram.objects.bulk_create(diagrams)

    def test_q(self):
        params = {'q': 'Diagram 1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_name(self):
        params = {'name': ['Diagram 1', 'Diagram 2']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
