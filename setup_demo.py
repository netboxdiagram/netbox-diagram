import http.client
import json
import os
import sys
import urllib.parse


def get_env_var(name):
    value = os.environ.get(name)
    if not value:
        print(f"Error: Environment variable '{name}' is not set.", file=sys.stderr)
        sys.exit(1)
    return value


NETBOX_HOST = get_env_var("NETBOX_HOST")
API_TOKEN = get_env_var("API_TOKEN")


def get_from_netbox(endpoint, params=None):
    conn_class = http.client.HTTPConnection
    conn = conn_class(NETBOX_HOST)
    headers = {"Authorization": f"Token {API_TOKEN}", "Accept": "application/json"}

    url = endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)

    conn.request("GET", url, headers=headers)
    response = conn.getresponse()
    body = response.read().decode()
    conn.close()

    if response.status == 200:
        data = json.loads(body)
        return data["results"][0] if data["count"] > 0 else None
    raise Exception(f"GET {endpoint} failed ({response.status}): {body}")


def post_to_netbox(endpoint, payload):
    conn_class = http.client.HTTPConnection
    conn = conn_class(NETBOX_HOST)
    headers = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json", "Accept": "application/json"}

    json_payload = json.dumps(payload)
    conn.request("POST", endpoint, body=json_payload, headers=headers)
    response = conn.getresponse()
    body = response.read().decode()
    conn.close()

    if response.status in (200, 201):
        return json.loads(body)
    elif response.status == 400 and "already exists" in body:
        return None
    else:
        raise Exception(f"POST {endpoint} failed ({response.status}): {body}")


def get_or_create_manufacturer(name, slug):
    url = "/api/dcim/manufacturers/"
    payload = {"name": name, "slug": slug}

    existing = get_from_netbox(url, {"slug": slug})
    return existing or post_to_netbox(url, payload)


def get_or_create_site(name, slug):
    url = "/api/dcim/sites/"
    payload = {"name": name, "slug": slug}

    existing = get_from_netbox(url, {"slug": slug})
    return existing or post_to_netbox(url, payload)


def get_or_create_device_role(name, slug):
    url = "/api/dcim/device-roles/"
    payload = {"name": name, "slug": slug}

    existing = get_from_netbox(url, {"slug": slug})
    return existing or post_to_netbox(url, payload)


def get_or_create_device_type(model, slug, manufacturer_id):
    url = "/api/dcim/device-types/"
    payload = {"model": model, "slug": slug, "manufacturer": manufacturer_id}

    existing = get_from_netbox(url, {"slug": slug})
    return existing or post_to_netbox(url, payload)


def get_or_create_interface_template(name, device_type_id, type="1000base-t"):
    url = "/api/dcim/interface-templates/"
    payload = {"name": name, "device_type": device_type_id, "type": type}

    existing = get_from_netbox(url, {"name": name, "device_type_id": device_type_id})
    return existing or post_to_netbox(url, payload)


def create_interface_templates_for_device_type(device_type_id, interface_names):
    created = []
    for name in interface_names:
        iface = get_or_create_interface_template(name, device_type_id)
        if iface:
            created.append(iface["name"])
    return created


def get_or_create_rearport_template(name, positions, device_type_id, type="8p8c"):
    url = "/api/dcim/rear-port-templates/"
    payload = {"name": name, "device_type": device_type_id, "positions": positions, "type": type}

    existing = get_from_netbox(url, {"name": name, "device_type_id": device_type_id})
    return existing or post_to_netbox(url, payload)


def get_or_create_frontport_template(name, position, rear_port, device_type_id, type="8p8c"):
    url = "/api/dcim/front-port-templates/"
    payload = {
        "name": name,
        "device_type": device_type_id,
        "rear_port_position": position,
        "rear_port": {"name": rear_port},
        "type": type,
    }

    existing = get_from_netbox(url, {"name": name, "device_type_id": device_type_id})

    return existing or post_to_netbox(url, payload)


def create_odfport_templates_for_device_type(device_type_id, front_ports, rear_ports):
    created = []
    for port in rear_ports:
        iface = get_or_create_rearport_template(port["name"], port["positions"], device_type_id)
        if iface:
            created.append(iface["name"])

    for port in front_ports:
        iface = get_or_create_frontport_template(port["name"], port["position"], port["rear_port"], device_type_id)
        if iface:
            created.append(iface["name"])
    return created


def get_or_create_device(name, device_type_id, device_role_id, site_id, status="active"):
    url = "/api/dcim/devices/"
    payload = {"name": name, "device_type": device_type_id, "role": device_role_id, "site": site_id, "status": status}

    existing = get_from_netbox(url, {"name": name})
    return existing or post_to_netbox(url, payload)


def get_interface(device_id, name):
    url = "/api/dcim/interfaces/"
    payload = {"device_id": device_id, "name": name}

    return get_from_netbox(url, payload)


def get_frontport(device_id, name):
    url = "/api/dcim/front-ports/"
    payload = {"device_id": device_id, "name": name}

    return get_from_netbox(url, payload)


def get_rearport(device_id, name):
    url = "/api/dcim/rear-ports/"
    payload = {"device_id": device_id, "name": name}

    return get_from_netbox(url, payload)


def get_or_create_provider(name, slug):
    url = "/api/circuits/providers/"
    payload = {"name": name, "slug": slug}

    existing = get_from_netbox(url, {"slug": slug})
    return existing or post_to_netbox(url, payload)


def get_or_create_circuit_type(name, slug):
    url = "/api/circuits/circuit-types/"
    payload = {"name": name, "slug": slug}

    existing = get_from_netbox(url, {"slug": slug})
    return existing or post_to_netbox(url, payload)


def get_or_create_circuit(provider_id, cid, circuit_type="Internet"):
    url = "/api/circuits/circuits/"
    payload = {"provider": provider_id, "cid": cid, "type": circuit_type}

    existing = get_from_netbox(url, {"cid": cid})
    return existing or post_to_netbox(url, payload)


def create_circuit_termination(circuit_id, term_side, site_id):
    url = "/api/circuits/circuit-terminations/"
    payload = {
        "circuit": circuit_id,
        "term_side": term_side,
        "termination_type": "dcim.site",
        "termination_id": site_id,
    }

    existing = get_from_netbox(url, {"cid": circuit_id, "term_side": term_side})
    return existing or post_to_netbox(url, payload)


def create_cable(a_type, a_id, b_type, b_id, label="uplink", cable_type="cat6"):
    url = "/api/dcim/cables/"
    payload = {
        "a_terminations": [{"object_type": a_type, "object_id": a_id}],
        "b_terminations": [{"object_type": b_type, "object_id": b_id}],
        "type": cable_type,
        "label": label,
    }

    existing = get_from_netbox(
        url,
        {
            "termination_a_type": a_type,
            "termination_a_id": a_id,
            "termination_b_type": b_type,
            "termination_b_id": b_id,
        },
    )

    return existing or post_to_netbox(url, payload)


def get_or_create_diagram(name):
    url = "/api/plugins/diagram/diagram/"
    payload = {"name": name, "description": "Automatically setup"}

    existing = get_from_netbox(url, {"name": name})
    return existing or post_to_netbox(url, payload)


def get_or_create_diagramassociation(diagram_id, object_type, object_id, coord_x=20, coord_y=20):
    url = "/api/plugins/diagram/diagramassociation/"
    payload = {
        "diagram": diagram_id,
        "assigned_object_type": object_type,
        "assigned_object_id": object_id,
        "coord_x": coord_x,
        "coord_y": coord_y,
    }

    object_type_id = 45

    existing = get_from_netbox(
        url,
        {
            "diagram": diagram_id,
            "assigned_object_type": object_type_id,
            "assigned_object_id": object_id,
        },
    )

    return existing or post_to_netbox(url, payload)


def main():
    print("Starting setup...")
    try:
        site = get_or_create_site("New York", "new-york")

        role = get_or_create_device_role("Core Switch", "core-switch")

        manufacturer = get_or_create_manufacturer("Cisco", "cisco")
        manufacturer_generic = get_or_create_manufacturer("Generic", "generic")

        device_type_c9300 = get_or_create_device_type("Cisco 9300", "cisco-9300", manufacturer["id"])
        device_type_odf = get_or_create_device_type("ODF", "odf", manufacturer_generic["id"])

        interfaces = [f"GigabitEthernet0/{i}" for i in range(0, 5)] + ["Mgmt0"]
        create_interface_templates_for_device_type(device_type_c9300["id"], interfaces)

        rear_ports = [{"name": "Line", "positions": 6}]
        front_ports = [{"name": f"Ch{i}", "position": i, "rear_port": rear_ports[0]["name"]} for i in range(0, 5)]

        create_odfport_templates_for_device_type(device_type_odf["id"], front_ports, rear_ports)

        for x in range(1, 6):
            name = f"core-switch-ny0{x}"
            get_or_create_device(
                name=name, device_type_id=device_type_c9300["id"], device_role_id=role["id"], site_id=site["id"]
            )

        for x in range(1, 3):
            name = f"ODF0{x}"
            get_or_create_device(
                name=name, device_type_id=device_type_odf["id"], device_role_id=role["id"], site_id=site["id"]
            )

        provider = get_or_create_provider("Speedy", "speedy")
        circuit_type = get_or_create_circuit_type("Internet", "internet")
        circuit_1 = get_or_create_circuit(provider["id"], "1", circuit_type=circuit_type["id"])

        device1 = get_from_netbox("/api/dcim/devices/", {"name": "core-switch-ny01"})
        device2 = get_from_netbox("/api/dcim/devices/", {"name": "core-switch-ny02"})
        device3 = get_from_netbox("/api/dcim/devices/", {"name": "core-switch-ny03"})
        device4 = get_from_netbox("/api/dcim/devices/", {"name": "core-switch-ny04"})
        device5 = get_from_netbox("/api/dcim/devices/", {"name": "core-switch-ny05"})

        odf01 = get_from_netbox("/api/dcim/devices/", {"name": "ODF01"})
        odf02 = get_from_netbox("/api/dcim/devices/", {"name": "ODF02"})

        device1_iface0 = get_interface(device1["id"], "GigabitEthernet0/0")
        device2_iface0 = get_interface(device2["id"], "GigabitEthernet0/0")
        device2_iface2 = get_interface(device2["id"], "GigabitEthernet0/2")
        device4_iface2 = get_interface(device4["id"], "GigabitEthernet0/2")

        device1_mgmt = get_interface(device1["id"], "Mgmt0")
        device2_mgmt = get_interface(device2["id"], "Mgmt0")
        device3_mgmt = get_interface(device3["id"], "Mgmt0")
        device4_mgmt = get_interface(device4["id"], "Mgmt0")

        device5_iface0 = get_interface(device5["id"], "GigabitEthernet0/0")
        device5_iface1 = get_interface(device5["id"], "GigabitEthernet0/1")
        device5_iface2 = get_interface(device5["id"], "GigabitEthernet0/2")
        device5_iface3 = get_interface(device5["id"], "GigabitEthernet0/3")

        odf01_front_ch01 = get_frontport(odf01["id"], "Ch0")
        odf01_line = get_rearport(odf01["id"], "Line")
        odf02_front_ch01 = get_frontport(odf02["id"], "Ch0")
        odf02_line = get_rearport(odf02["id"], "Line")

        circuit_termination_a = create_circuit_termination(circuit_1["id"], "A", site["id"])
        circuit_termination_z = create_circuit_termination(circuit_1["id"], "Z", site["id"])

        create_cable(
            a_type="dcim.interface",
            a_id=device1_iface0["id"],
            b_type="circuits.circuittermination",
            b_id=circuit_termination_a["id"],
        )
        create_cable(
            a_type="dcim.interface",
            a_id=device2_iface0["id"],
            b_type="circuits.circuittermination",
            b_id=circuit_termination_z["id"],
        )

        create_cable(
            a_type="dcim.interface", a_id=device1_mgmt["id"], b_type="dcim.interface", b_id=device5_iface0["id"]
        )
        create_cable(
            a_type="dcim.interface", a_id=device2_mgmt["id"], b_type="dcim.interface", b_id=device5_iface1["id"]
        )
        create_cable(
            a_type="dcim.interface", a_id=device3_mgmt["id"], b_type="dcim.interface", b_id=device5_iface2["id"]
        )
        create_cable(
            a_type="dcim.interface", a_id=device4_mgmt["id"], b_type="dcim.interface", b_id=device5_iface3["id"]
        )

        create_cable(
            a_type="dcim.interface", a_id=device2_iface2["id"], b_type="dcim.frontport", b_id=odf01_front_ch01["id"]
        )

        create_cable(
            a_type="dcim.interface", a_id=device4_iface2["id"], b_type="dcim.frontport", b_id=odf02_front_ch01["id"]
        )

        create_cable(a_type="dcim.rearport", a_id=odf01_line["id"], b_type="dcim.rearport", b_id=odf02_line["id"])

        create_cable(
            a_type="dcim.interface",
            a_id=device1_iface0["id"],
            b_type="circuits.circuittermination",
            b_id=circuit_termination_a["id"],
        )

        diagram = get_or_create_diagram("Demo diagram")
        get_or_create_diagramassociation(diagram["id"], "dcim.device", device1["id"], coord_x=200, coord_y=80)
        get_or_create_diagramassociation(diagram["id"], "dcim.device", device2["id"], coord_x=980, coord_y=80)
        get_or_create_diagramassociation(diagram["id"], "dcim.device", device3["id"], coord_x=200, coord_y=540)
        get_or_create_diagramassociation(diagram["id"], "dcim.device", device4["id"], coord_x=980, coord_y=540)
        get_or_create_diagramassociation(diagram["id"], "dcim.device", device5["id"], coord_x=620, coord_y=540)

        print("Setup done!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
