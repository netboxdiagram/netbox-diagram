# NetBox Diagram

**Automatically generated, up-to-date network diagrams from NetBox**

![CI Status](https://github.com/netboxdiagram/netbox_diagram/actions/workflows/ci.yml/badge.svg)
![Test Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/netboxdiagram/6a925b197e40e7e27cd577a4abd5b586/raw/a52ac8a432242f3bd7af5f3b061e67571c479b96/cov.json)
![Supported Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Supported NetBox Versions](https://img.shields.io/badge/NetBox-4.x-blue.svg)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## 📑 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#-installation)
- [Quick Demo](#-quick-demo)
- [Screenshots](#-screenshots)

---

## Overview

**`netbox_diagram`** is a plugin for [NetBox](https://netbox.dev) that enables the creation and management of network diagrams using NetBox devices and circuits. It renders physical and logical interconnections (e.g., cables, circuits) between devices based on their coordinates and metadata.

### Key Features

- Group devices into diagrams
- Automatically render cables and circuits
- Position devices using X/Y coordinates
- Asynchronous updates for fast performance
- Toggle grid and link labels for clarity

> ❗ **Limitations:**
>
> - No support for virtual machines
> - Power connections and patch panels are not visualized

For more advanced or flexible diagramming, consider:

- [NextBox UI Plugin](https://github.com/iDebugAll/nextbox-ui-plugin)
- [NetBox Topology Views Plugin](https://github.com/netbox-community/netbox-topology-views)

---

## 🔧 Installation

### 1. Install via `pip`

```bash
pip install netbox_diagram
```

### 2. Enable the plugin in `configuration.py`

```python
PLUGINS = [
    'netbox_diagram',
    # other plugins...
]
```

### 3. Apply migrations and collect static files

```bash
python3 manage.py migrate
python3 manage.py collectstatic
```

### 4. Restart NetBox

```bash
sudo systemctl restart netbox
```

---

## 🚀 Quick Demo

Want to try it out quickly? Use the provided demo script to set up a sample environment. A running Netbox instance is required though!

This will:

- Create 5 devices
- Connect 2 devices via a circuit
- Simulate patch panels via front-back port connections
- Connect 4 devices to one central device
- Generate a diagram including all devices

### Run the demo

> 📌 Requires a running NetBox instance with API access enabled.

Update NETBOX_HOST and API_TOKEN to match your environment. (it obviously should point to your Netbox and use a API Token you've generated). The script itself has no external dependencies, you can run it straight away.

```bash
export NETBOX_HOST="172.16.123.1:8001"
export API_TOKEN="your_token_here"
python3 setup_demo.py
```

---

## 📸 Screenshots

Diagram overview with name, description, and associated objects:  
![Diagram Overview](img/diagram_overview.png)

Final generated diagram (patch panels not shown):  
![Final Diagram](img/diagram.png)

Diagram with link labels disabled:  
![Diagram No Labels](img/diagram_no_label.png)

Diagram with grid enabled:  
![Diagram with Grid](img/diagram_grid.png)

New "Diagrams" tab on Device and Circuit detail pages:
![Device Diagram Tab](img/device_diagram.png)

![Circuit Diagram Tab](img/circuits_diagram.png)
