import json

from circuits.models import Circuit, CircuitType, Provider
from dcim.models import Device
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from utilities.testing import ViewTestCases, create_test_device
from utilities.testing.utils import create_test_user

from netbox_diagram.models import Diagram, DiagramAssociation


class DiagramTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = Diagram

    @classmethod
    def setUpTestData(cls):
        diagrams = (
            Diagram(name="Diagram 1"),
            Diagram(name="Diagram 2"),
            Diagram(name="Diagram 3"),
        )
        Diagram.objects.bulk_create(diagrams)

        cls.form_data = {
            "name": "Diagram X",
        }

        cls.bulk_edit_data = {
            "description": "A Diagram Description",
        }

    def _get_base_url(self):
        return "plugins:netbox_diagram:diagram_{}"


class DiagramAssociationTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = DiagramAssociation

    @classmethod
    def setUpTestData(cls):
        device_1 = create_test_device(name="Test Device for View #1")
        device_2 = create_test_device(name="Test Device for View #2")
        device_3 = create_test_device(name="Test Device for View #3")

        diagram = Diagram.objects.create(name="Diagram View")
        device_ct = ContentType.objects.get_for_model(Device)

        # Create the diagramassociation
        diagramassociations = (
            DiagramAssociation(diagram=diagram, assigned_object_type=device_ct, assigned_object_id=device_1.id),
            DiagramAssociation(diagram=diagram, assigned_object_type=device_ct, assigned_object_id=device_2.id),
        )
        DiagramAssociation.objects.bulk_create(diagramassociations)

        cls.form_data = {
            "diagram": diagram.pk,
            "device": device_3.id,
        }

        cls.bulk_edit_data = {
            "coord_x": 90,
        }

    def _get_base_url(self):
        return "plugins:netbox_diagram:diagramassociation_{}"


class DiagramDataViewTest(TestCase):
    def setUp(self):
        # Set up test data
        provider = Provider.objects.create(name="Provider 1", slug="provider-1")
        circuittype = CircuitType.objects.create(name="Circuit Type 1", slug="circuit-type-1")
        self.circuit = Circuit.objects.create(provider=provider, type=circuittype, cid="1")
        self.diagram = Diagram.objects.create(name="Test Diagram")

        # Create a test user with all needed permissions
        self.user = create_test_user(
            permissions=[
                "circuits.add_circuit",
                "circuits.view_circuit",
                "netbox_diagram.add_diagramassociation",
                "netbox_diagram.change_diagramassociation",
                "netbox_diagram.view_diagramassociation",
                "netbox_diagram.view_diagram",
            ]
        )
        self.client.force_login(self.user)

    def test_get_diagram_data(self):
        url = reverse("plugins:netbox_diagram:diagram_data", kwargs={"pk": self.diagram.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_post_creates_and_updates_association(self):
        # Post data simulating a node needing association
        post_data = [{"type": "circuit", "name": self.circuit.cid, "x": 150, "y": 250, "association_id": None}]

        url = reverse("plugins:netbox_diagram:diagram_data", kwargs={"pk": self.diagram.pk})
        response = self.client.post(url, json.dumps(post_data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

        # Ensure the DiagramAssociation was created and coordinates match
        assoc = DiagramAssociation.objects.first()
        self.assertIsNotNone(assoc)
        self.assertEqual(assoc.coord_x, 150)
        self.assertEqual(assoc.coord_y, 250)

    def test_post_updates_existing_association(self):
        # Create existing association
        obj_type = ContentType.objects.get_for_model(self.circuit)
        assoc = DiagramAssociation.objects.create(
            diagram=self.diagram,
            assigned_object_type=obj_type,
            assigned_object_id=self.circuit.id,
            coord_x=100,
            coord_y=200,
        )

        post_data = [{"type": "circuit", "name": self.circuit.cid, "x": 300, "y": 400, "association_id": assoc.id}]

        url = reverse("plugins:netbox_diagram:diagram_data", kwargs={"pk": self.diagram.pk})
        response = self.client.post(url, json.dumps(post_data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        assoc.refresh_from_db()
        self.assertEqual(assoc.coord_x, 300)
        self.assertEqual(assoc.coord_y, 400)
