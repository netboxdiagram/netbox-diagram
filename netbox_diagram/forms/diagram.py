from circuits.models import Circuit
from dcim.models import Device
from django import forms
from django.utils.translation import gettext as _
from netbox.forms import NetBoxModelBulkEditForm, NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet, TabbedGroups

from netbox_diagram.models import Diagram, DiagramAssociation

_all_ = (
    'DiagramForm',
    'DiagramBulkEditForm',
    'DiagramFilterForm',
    'DiagramAssociationForm',
    'DiagramAssociationBulkEditForm',
    'DiagramAssociationFilterForm',
)


class DiagramForm(NetBoxModelForm):
    class Meta:
        model = Diagram
        fields = ('name', 'description')


class DiagramBulkEditForm(NetBoxModelBulkEditForm):
    model = Diagram
    description = forms.CharField(label=_('Description'), max_length=200, required=False)

    fieldsets = (FieldSet('description'),)
    nullable_fields = ('description',)


class DiagramFilterForm(NetBoxModelFilterSetForm):
    model = Diagram
    fieldsets = (
        FieldSet('q', 'filter_id'),
        FieldSet('name', 'description', name=_('Diagrams')),
    )

    tag = TagFilterField(model)


class DiagramAssociationForm(NetBoxModelForm):
    diagram = DynamicModelChoiceField(
        queryset=Diagram.objects.all(),
        selector=False,
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
        # Todo: filter devices that are already associated?
    )
    circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
        selector=True,
        label=_('Circuit'),
        # Todo: filter devices that are already associated?
    )
    coord_x = forms.IntegerField(required=False, label=_('X coordinate'))
    coord_y = forms.IntegerField(required=False, label=_('Y coordinate'))

    fieldsets = (
        FieldSet('diagram', 'coord_x', 'coord_y', name=_('Generic')),
        FieldSet(
            TabbedGroups(
                FieldSet('device', name=_('Device')),
                FieldSet('circuit', name=_('Circuit')),
            ),
            name=_('Assignment'),
        ),
    )

    class Meta:
        model = DiagramAssociation
        fields = (
            'diagram',
            'device',
            'circuit',
            'coord_x',
            'coord_y',
        )

    def __init__(self, *args, **kwargs):
        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            type_to_field = {
                Device: 'device',
                Circuit: 'circuit',
            }

            for obj_type, field_name in type_to_field.items():
                if isinstance(instance.assigned_object, obj_type):
                    initial[field_name] = instance.assigned_object
                    break

        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Handle object assignment
        selected_objects = [field for field in ('device', 'circuit') if self.cleaned_data[field]]
        if len(selected_objects) > 1:
            raise forms.ValidationError({selected_objects[1]: _('An IP address can only be assigned to a single object.')})
        elif selected_objects:
            self.instance.assigned_object = self.cleaned_data[selected_objects[0]]
        else:
            self.instance.assigned_object = None


class DiagramAssociationBulkEditForm(NetBoxModelBulkEditForm):
    model = DiagramAssociation

    coord_x = forms.IntegerField(required=False, label=_('X coordinate'))
    coord_y = forms.IntegerField(required=False, label=_('Y coordinate'))

    fieldsets = (FieldSet('coord_x', 'coord_y', name=_('Generic')),)

    class Meta:
        model = DiagramAssociation
        fields = (
            'coord_x',
            'coord_y',
        )

    def __init__(self, *args, **kwargs):
        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()

        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)


class DiagramAssociationFilterForm(NetBoxModelFilterSetForm):
    model = DiagramAssociation
    fieldsets = (
        FieldSet('q', 'filter_id'),
        FieldSet('diagram', name=_('Diagrams')),
    )

    tag = TagFilterField(model)
