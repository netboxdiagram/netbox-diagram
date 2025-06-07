from circuits.models import Circuit
from dcim.models import Device
from netbox.views import generic
from utilities.views import ViewTab, register_model_view

# from netbox_diagram.filtersets import *
# from netbox_diagram.tables import *


@register_model_view(Device, name='netbox_diagram', path='diagrams')
class DiagramDeviceTabView(generic.ObjectView):
    queryset = Device.objects.all()
    template_name = 'netbox_diagram/diagramtab.html'
    tab = ViewTab(label='Diagrams')


@register_model_view(Circuit, name='netbox_diagram', path='diagrams')
class DiagramCircuitTabView(generic.ObjectView):
    queryset = Circuit.objects.all()
    template_name = 'netbox_diagram/diagramtab.html'
    tab = ViewTab(label='Diagrams')
