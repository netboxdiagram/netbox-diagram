from netbox.views.generic import (
    BulkDeleteView,
    BulkEditView,
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView,
)
from utilities.views import register_model_view

from netbox_diagram.filtersets import DiagramAssociationFilterSet, DiagramFilterSet
from netbox_diagram.forms import (
    DiagramAssociationBulkEditForm,
    DiagramAssociationFilterForm,
    DiagramAssociationForm,
    DiagramBulkEditForm,
    DiagramFilterForm,
    DiagramForm,
)
from netbox_diagram.models import Diagram, DiagramAssociation
from netbox_diagram.tables import DiagramAssociationTable, DiagramTable

_all__ = (
    'DiagramListView',
    'DiagramView',
    'DiagramEditView',
    'DiagramBulkEditView',
    'DiagramDeleteView',
    'DiagramBulkDeleteView',
    'DiagramAssociationListView',
    'DiagramAssociationView',
    'DiagramAssociationEditView',
    'DiagramAssociationBulkEditView',
    'DiagramAssociationDeleteView',
    'DiagramAssociationBulkDeleteView',
)


# Diagram
@register_model_view(Diagram, name='list')
class DiagramListView(ObjectListView):
    """
    List view of all Diagram objects
    """

    queryset = Diagram.objects.all()
    table = DiagramTable
    filterset = DiagramFilterSet
    filterset_form = DiagramFilterForm


@register_model_view(Diagram)
class DiagramView(ObjectView):
    """
    Diagram object view
    """

    queryset = Diagram.objects.all()


@register_model_view(Diagram, 'edit')
class DiagramEditView(ObjectEditView):
    """
    Diagram Object Edit view
    """

    queryset = Diagram.objects.all()
    form = DiagramForm


@register_model_view(Diagram, 'bulk_edit')
class DiagramBulkEditView(BulkEditView):
    """
    Diagram Object Bulk Edit view
    """

    queryset = Diagram.objects.all()
    filterset = DiagramFilterSet
    table = DiagramTable
    form = DiagramBulkEditForm


@register_model_view(Diagram, 'delete')
class DiagramDeleteView(ObjectDeleteView):
    queryset = Diagram.objects.all()


@register_model_view(Diagram, 'bulk_delete')
class DiagramBulkDeleteView(BulkDeleteView):
    """
    Diagram Object Bulk Delete view
    """

    queryset = Diagram.objects.all()
    filterset = DiagramFilterSet
    table = DiagramTable


# DiagramAssociation
@register_model_view(DiagramAssociation, name='list')
class DiagramAssociationListView(ObjectListView):
    """
    List view of all DiagramAssociation objects
    """

    queryset = DiagramAssociation.objects.all()
    table = DiagramAssociationTable
    filterset = DiagramAssociationFilterSet
    filterset_form = DiagramAssociationFilterForm


@register_model_view(DiagramAssociation)
class DiagramAssociationView(ObjectView):
    """
    DiagramAssociation object view
    """

    queryset = DiagramAssociation.objects.all()


@register_model_view(DiagramAssociation, 'edit')
class DiagramAssociationEditView(ObjectEditView):
    """
    DiagramAssociation Object Edit view
    """

    queryset = DiagramAssociation.objects.all()
    form = DiagramAssociationForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if 'device' in request.GET:
            try:
                obj.assigned_object = Device.objects.get(pk=request.GET['device'])
            except (ValueError, Device.DoesNotExist):
                pass
        elif 'circuit' in request.GET:
            try:
                obj.assigned_object = Circuit.objects.get(pk=request.GET['circuit'])
            except (ValueError, Circuit.DoesNotExist):
                pass

        return obj


@register_model_view(DiagramAssociation, 'bulk_edit')
class DiagramAssociationBulkEditView(BulkEditView):
    """
    DiagramAssociation Object Bulk Edit view
    """

    queryset = DiagramAssociation.objects.all()
    filterset = DiagramAssociationFilterSet
    table = DiagramAssociationTable
    form = DiagramAssociationBulkEditForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if 'device' in request.GET:
            try:
                obj.assigned_object = Device.objects.get(pk=request.GET['device'])
            except (ValueError, Device.DoesNotExist):
                pass
        elif 'circuit' in request.GET:
            try:
                obj.assigned_object = Circuit.objects.get(pk=request.GET['circuit'])
            except (ValueError, Circuit.DoesNotExist):
                pass

        return obj


@register_model_view(DiagramAssociation, 'delete')
class DiagramAssociationDeleteView(ObjectDeleteView):
    queryset = DiagramAssociation.objects.all()


@register_model_view(DiagramAssociation, 'bulk_delete')
class DiagramAssociationBulkDeleteView(BulkDeleteView):
    """
    DiagramAssociation Object Bulk Delete view
    """

    queryset = DiagramAssociation.objects.all()
    filterset = DiagramAssociationFilterSet
    table = DiagramAssociationTable
