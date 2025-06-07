from dcim.models import Device
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from utilities.testing import APITestCase, APIViewTestCases, create_test_device

from netbox_diagram.models import Diagram, DiagramAssociation


class AppTest(APITestCase):
    def test_root(self):
        url = reverse('plugins-api:netbox_diagram-api:api-root')
        response = self.client.get(f'{url}?format=api', **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DiagramTest(APIViewTestCases.APIViewTestCase):
    model = Diagram
    view_namespace = 'plugins-api:netbox_diagram'
    brief_fields = ['description', 'display', 'id', 'name', 'url']

    create_data = [
        {
            'name': 'Diagram 4',
        },
        {
            'name': 'Diagram 5',
        },
        {
            'name': 'Diagram 6',
        },
    ]
    bulk_update_data = {'description': 'New description'}

    @classmethod
    def setUpTestData(cls):
        diagrams = [
            Diagram(name='Diagram 1'),
            Diagram(name='Diagram 2'),
            Diagram(name='Diagram 3'),
        ]
        Diagram.objects.bulk_create(diagrams)

    def test_graphql_get_object(self):
        """Not implemented"""
        pass

    def test_graphql_list_object(self):
        """Not implemented"""
        pass

    def test_graphql_list_objects(self):
        """Not implemented"""
        pass


class DiagramAssociationTest(APIViewTestCases.APIViewTestCase):
    model = DiagramAssociation
    view_namespace = 'plugins-api:netbox_diagram'
    brief_fields = [
        'assigned_object',
        'assigned_object_id',
        'assigned_object_type',
        'coord_x',
        'coord_y',
        'diagram',
        'display',
        'id',
        'url',
    ]

    bulk_update_data = {'description': 'New description'}

    @classmethod
    def setUpTestData(cls):
        # super().setUpTestData()

        pre_created_diagrams = Diagram.objects.bulk_create(
            [
                Diagram(name='Precreated Diagram 1'),
                Diagram(name='Precreated Diagram 2'),
                Diagram(name='Precreated Diagram 3'),
            ]
        )
        pre_created_devices = [create_test_device(name=f'Precreated Device {i}') for i in range(1, 4)]
        device_ct = ContentType.objects.get_for_model(Device)

        for i in range(3):
            DiagramAssociation.objects.create(
                diagram=pre_created_diagrams[i],
                assigned_object_type=device_ct,
                assigned_object_id=pre_created_devices[i].id,
            )

        cls.create_data = []
        new_diagrams = Diagram.objects.bulk_create(
            [
                Diagram(name='Diagram 4'),
                Diagram(name='Diagram 5'),
                Diagram(name='Diagram 6'),
            ]
        )
        new_devices = [create_test_device(name=f'Device {i}') for i in range(4, 7)]

        for i in range(3):
            cls.create_data.append(
                {
                    'diagram': new_diagrams[i].id,
                    'assigned_object_type': f'{device_ct.app_label}.{device_ct.model}',
                    'assigned_object_id': new_devices[i].id,
                }
            )

        cls.bulk_update_data = {'coord_y': 80}

    def test_graphql_get_object(self):
        """Not implemented"""
        pass

    def test_graphql_list_object(self):
        """Not implemented"""
        pass

    def test_graphql_list_objects(self):
        """Not implemented"""
        pass
