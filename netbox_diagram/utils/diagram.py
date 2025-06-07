from circuits.models import Circuit, CircuitTermination
from dcim.models import Cable, Device, FrontPort, Interface, RearPort

from netbox_diagram.models import DiagramAssociation


def compute_diagram_data(diagram_id):
    associated_nodes = DiagramAssociation.objects.filter(diagram_id=diagram_id)
    nodes, edges, applicable_devices, device_ids = [], [], [], []

    for node in associated_nodes:
        device = node.assigned_object
        if not isinstance(device, (Device, Circuit)):
            continue

        device_name = getattr(device, 'name', None) or getattr(device, 'cid', None)
        applicable_devices.append(device)
        device_ids.append(device.pk)
        nodes.append(
            {
                'name': device_name,
                'association_id': node.id,
                'type': 'device',
                'x': node.coord_x,
                'y': node.coord_y,
            }
        )

    node_names = {node['name'] for node in nodes}
    device_positions = {node['name']: (node['x'], node['y']) for node in nodes}

    def resolve_connected_interface(termination, visited=None):
        if visited is None:
            visited = set()
        if not termination or termination in visited:
            return None
        visited.add(termination)

        if isinstance(termination, Interface):
            return termination
        if isinstance(termination, FrontPort):
            cable = getattr(termination, 'cable', None)
            if cable:
                for term in cable.terminations.all():
                    if term.termination != termination:
                        return resolve_connected_interface(term.termination, visited)
            if termination.rear_port:
                return resolve_connected_interface(termination.rear_port, visited)
        if isinstance(termination, RearPort):
            for front_port in termination.frontports.all():
                cable = getattr(front_port, 'cable', None)
                if cable:
                    for term in cable.terminations.all():
                        if term.termination != front_port:
                            return resolve_connected_interface(term.termination, visited)
        return None

    def add_circuit_node_if_missing(circuit_name, connected_device_names):
        if circuit_name in node_names:
            return
        coords = [device_positions[d] for d in connected_device_names if d in device_positions]
        x, y = (
            (
                int(sum(x for x, y in coords) / len(coords) + 50),
                int(sum(y for x, y in coords) / len(coords) + 50),
            )
            if coords
            else (0, 0)
        )
        nodes.append(
            {
                'name': circuit_name,
                'association_id': None,
                'x': x,
                'y': y,
                'type': 'circuit',
            }
        )
        node_names.add(circuit_name)
        device_positions[circuit_name] = (x, y)

    for cable in Cable.objects.prefetch_related('terminations__termination'):
        terms = list(cable.terminations.all())
        if len(terms) < 2:
            continue
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                iface_a = resolve_connected_interface(terms[i].termination)
                iface_b = resolve_connected_interface(terms[j].termination)

                if iface_a and iface_b and isinstance(iface_a, Interface) and isinstance(iface_b, Interface):
                    if iface_a.device_id == iface_b.device_id and iface_a.name == iface_b.name:
                        continue
                    if iface_a.device_id in device_ids or iface_b.device_id in device_ids:
                        edges.append(
                            {
                                'source': iface_a.device.name,
                                'target': iface_b.device.name,
                                'description': f'{iface_a.device.name}:{iface_a.name} ↔ {iface_b.device.name}:{iface_b.name}',
                            }
                        )
                elif (iface_a and isinstance(terms[j].termination, CircuitTermination)) or (iface_b and isinstance(terms[i].termination, CircuitTermination)):
                    iface = iface_a if iface_a else iface_b
                    cterm = terms[j].termination if isinstance(terms[j].termination, CircuitTermination) else terms[i].termination
                    circuit = cterm.circuit
                    if iface.device_id in device_ids:
                        add_circuit_node_if_missing(circuit.cid, [iface.device.name])
                        edges.append(
                            {
                                'source': iface.device.name,
                                'target': circuit.cid,
                                'description': f'{iface.device.name}:{iface.name} ↔ Circuit {circuit.cid}',
                            }
                        )

    visited_pairs = set()
    for term_a in CircuitTermination.objects.select_related('circuit').filter(circuit__terminations__isnull=False):
        for term_b in term_a.circuit.terminations.exclude(pk=term_a.pk):
            dev_a = getattr(term_a.termination, 'device', None)
            dev_b = getattr(term_b.termination, 'device', None)
            if not dev_a or not dev_b:
                continue
            circuit_name = term_a.circuit.cid
            add_circuit_node_if_missing(circuit_name, [dev_a.name, dev_b.name])
            pair_key = tuple(sorted([dev_a.pk, dev_b.pk]))
            if pair_key in visited_pairs:
                continue
            visited_pairs.add(pair_key)
            if dev_a.pk in device_ids or dev_b.pk in device_ids:
                edges.append(
                    {
                        'source': dev_a.name,
                        'target': dev_b.name,
                        'description': f'Via Circuit {circuit_name}',
                    }
                )

    valid_names = {node['name'] for node in nodes}
    edges = [e for e in edges if e['source'] in valid_names and e['target'] in valid_names]
    return {'nodes': nodes, 'edges': edges}
