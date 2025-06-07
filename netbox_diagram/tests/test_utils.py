from circuits.models import Circuit, CircuitTermination, CircuitType, Provider
from dcim.models import Cable, Device, Interface
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from utilities.testing import create_test_device

from netbox_diagram.models import Diagram, DiagramAssociation
from netbox_diagram.utils.diagram import compute_diagram_data


class UtilsTestCase(TestCase):
    def test_diagramassociation_update_cable(self):
        # Create the devices
        device_1 = create_test_device(name='Device 1')
        device_2 = create_test_device(name='Device 2')

        interfaces = (
            Interface(device=device_1, name='eth0'),
            Interface(device=device_2, name='eth0'),
        )
        Interface.objects.bulk_create(interfaces)

        device_ct = ContentType.objects.get_for_model(Device)
        diagram = Diagram.objects.create(name='Util Diagram', description='Demo Description')
        # Create the diagramassociation
        diagramassociation_1 = DiagramAssociation(
            diagram=diagram,
            assigned_object_type=device_ct,
            assigned_object_id=device_1.id,
        )
        diagramassociation_1.full_clean()
        diagramassociation_1.save()

        diagramassociation_2 = DiagramAssociation(
            diagram=diagram,
            assigned_object_type=device_ct,
            assigned_object_id=device_2.id,
        )
        diagramassociation_2.full_clean()
        diagramassociation_2.save()

        # Create a cable between the nodes
        Cable.objects.create(a_terminations=[interfaces[0]], b_terminations=[interfaces[1]])

        # Update the cached_data by calling the fuction
        diagram.cached_data = compute_diagram_data(diagram.id)
        # Verify the data
        expected_json = {
            'nodes': [
                {
                    'name': device_1.name,
                    'association_id': diagramassociation_1.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': device_2.name,
                    'association_id': diagramassociation_2.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
            ],
            'edges': [
                {
                    'source': device_1.name,
                    'target': device_2.name,
                    'description': f'{device_1.name}:{interfaces[0].name} ↔ {device_2.name}:{interfaces[1].name}',
                }
            ],
        }

        self.assertEqual(diagram.cached_data, expected_json)

    def test_diagramassociation_associate_device(self):
        # Create the devices
        device_1 = create_test_device(name='Device 1')
        device_2 = create_test_device(name='Device 2')
        device_3 = create_test_device(name='Device 3')

        interfaces = (
            Interface(device=device_1, name='eth0'),
            Interface(device=device_2, name='eth0'),
            Interface(device=device_2, name='eth1'),
            Interface(device=device_3, name='eth1'),
        )
        Interface.objects.bulk_create(interfaces)

        device_ct = ContentType.objects.get_for_model(Device)
        diagram = Diagram.objects.create(name='Util Diagram', description='Demo Description')

        # Create the diagramassociation
        diagramassociation_1 = DiagramAssociation(
            diagram=diagram,
            assigned_object_type=device_ct,
            assigned_object_id=device_1.id,
        )
        diagramassociation_1.full_clean()
        diagramassociation_1.save()

        diagramassociation_2 = DiagramAssociation(
            diagram=diagram,
            assigned_object_type=device_ct,
            assigned_object_id=device_2.id,
        )
        diagramassociation_2.full_clean()
        diagramassociation_2.save()

        # Create a cable between the nodes
        Cable.objects.create(a_terminations=[interfaces[0]], b_terminations=[interfaces[1]])

        # Update the cached_data by calling the fuction
        diagram.cached_data = compute_diagram_data(diagram.id)
        # Verify the data from the first run
        expected_json = {
            'nodes': [
                {
                    'name': device_1.name,
                    'association_id': diagramassociation_1.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': device_2.name,
                    'association_id': diagramassociation_2.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
            ],
            'edges': [
                {
                    'source': device_1.name,
                    'target': device_2.name,
                    'description': f'{device_1.name}:{interfaces[0].name} ↔ {device_2.name}:{interfaces[1].name}',
                }
            ],
        }
        self.assertEqual(diagram.cached_data, expected_json)

        # Create a association
        diagramassociation_3 = DiagramAssociation(
            diagram=diagram,
            assigned_object_type=device_ct,
            assigned_object_id=device_3.id,
        )
        diagramassociation_3.full_clean()
        diagramassociation_3.save()

        # Update the cached_data by calling the fuction
        diagram.cached_data = compute_diagram_data(diagram.id)
        expected_json = {
            'nodes': [
                {
                    'name': device_1.name,
                    'association_id': diagramassociation_1.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': device_2.name,
                    'association_id': diagramassociation_2.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': device_3.name,
                    'association_id': diagramassociation_3.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
            ],
            'edges': [
                {
                    'source': device_1.name,
                    'target': device_2.name,
                    'description': f'{device_1.name}:{interfaces[0].name} ↔ {device_2.name}:{interfaces[1].name}',
                }
            ],
        }
        self.assertEqual(diagram.cached_data, expected_json)

        # Create a cable between the nodes
        Cable.objects.create(a_terminations=[interfaces[2]], b_terminations=[interfaces[3]])

        # Update the cached_data by calling the fuction
        diagram.cached_data = compute_diagram_data(diagram.id)
        expected_json = {
            'nodes': [
                {
                    'name': device_1.name,
                    'association_id': diagramassociation_1.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': device_2.name,
                    'association_id': diagramassociation_2.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': device_3.name,
                    'association_id': diagramassociation_3.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
            ],
            'edges': [
                {
                    'source': device_1.name,
                    'target': device_2.name,
                    'description': f'{device_1.name}:{interfaces[0].name} ↔ {device_2.name}:{interfaces[1].name}',
                },
                {
                    'source': device_2.name,
                    'target': device_3.name,
                    'description': f'{device_2.name}:{interfaces[2].name} ↔ {device_3.name}:{interfaces[3].name}',
                },
            ],
        }
        self.assertEqual(diagram.cached_data, expected_json)

    # WIP
    def test_diagramassociation_circuit_termination(self):
        # Create the devices
        device_1 = create_test_device(name='Device 1')
        device_2 = create_test_device(name='Device 2')

        interfaces = (
            Interface(device=device_1, name='eth0'),
            Interface(device=device_2, name='eth0'),
        )
        Interface.objects.bulk_create(interfaces)

        device_ct = ContentType.objects.get_for_model(Device)
        diagram = Diagram.objects.create(name='Util Diagram', description='Demo Description')

        # Create the diagramassociation
        diagramassociation_1 = DiagramAssociation(
            diagram=diagram,
            assigned_object_type=device_ct,
            assigned_object_id=device_1.id,
        )
        diagramassociation_1.full_clean()
        diagramassociation_1.save()

        diagramassociation_2 = DiagramAssociation(
            diagram=diagram,
            assigned_object_type=device_ct,
            assigned_object_id=device_2.id,
        )
        diagramassociation_2.full_clean()
        diagramassociation_2.save()

        # Create a Circuit
        provider = Provider.objects.create(name='Provider 1', slug='provider-1')
        circuittype = CircuitType.objects.create(name='Circuit Type 1', slug='circuit-type-1')
        circuit1 = Circuit.objects.create(provider=provider, type=circuittype, cid='1')
        circuittermination1 = CircuitTermination.objects.create(circuit=circuit1, termination=device_1.site, term_side='A')
        circuittermination2 = CircuitTermination.objects.create(circuit=circuit1, termination=device_2.site, term_side='Z')

        # Terminate Device 1 to Circuit side A
        Cable.objects.create(a_terminations=[interfaces[0]], b_terminations=[circuittermination1])
        # Terminate Device 2 to Circuit side Z
        Cable.objects.create(a_terminations=[interfaces[1]], b_terminations=[circuittermination2])
        # Update the cached_data by calling the fuction
        diagram.cached_data = compute_diagram_data(diagram.id)
        # Verify the data
        expected_json = {
            'nodes': [
                {
                    'name': device_1.name,
                    'association_id': diagramassociation_1.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': device_2.name,
                    'association_id': diagramassociation_2.id,
                    'type': 'device',
                    'x': 20,
                    'y': 20,
                },
                {
                    'name': circuit1.cid,
                    'association_id': None,
                    'x': 70,
                    'y': 70,
                    'type': 'circuit',
                },
            ],
            'edges': [
                {
                    'source': device_1.name,
                    'target': '1',
                    'description': f'{device_1.name}:{interfaces[0].name} ↔ Circuit {circuit1.cid}',
                },
                {
                    'source': device_2.name,
                    'target': '1',
                    'description': f'{device_2.name}:{interfaces[1].name} ↔ Circuit {circuit1.cid}',
                },
            ],
        }

        self.assertEqual(diagram.cached_data, expected_json)
