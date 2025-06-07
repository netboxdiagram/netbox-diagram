from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from netbox_diagram.models import *
from netbox_diagram.views import *
from netbox_diagram.views.jobs import TriggerDiagramCacheJobView

urlpatterns = [
    path('diagramdata/<int:pk>', DiagramData.as_view(), name='diagram_data'),
    path('', DiagramListView.as_view(), name='diagram_list'),
    path('diagram/<int:pk>/', DiagramView.as_view(), name='diagram'),
    path('diagram/<int:pk>/edit', DiagramEditView.as_view(), name='diagram_edit'),
    path('diagram/<int:pk>/delete', DiagramDeleteView.as_view(), name='diagram_delete'),
    path('diagram/<int:pk>/update-cache/', TriggerDiagramCacheJobView.as_view(), name='diagram_update_cache'),
    path('diagram/add', DiagramEditView.as_view(), name='diagram_add'),
    path('diagram/edit', DiagramBulkEditView.as_view(), name='diagram_bulk_edit'),
    path('diagram/delete', DiagramBulkDeleteView.as_view(), name='diagram_bulk_delete'),
    path('diagram/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='diagram_changelog', kwargs={'model': Diagram}),
    path('diagramassociation', DiagramAssociationListView.as_view(), name='diagramassociation_list'),
    path('diagramassociation/<int:pk>/', DiagramAssociationView.as_view(), name='diagramassociation'),
    path('diagramassociation/<int:pk>/edit', DiagramAssociationEditView.as_view(), name='diagramassociation_edit'),
    path('diagramassociation/<int:pk>/delete', DiagramAssociationDeleteView.as_view(), name='diagramassociation_delete'),
    path('diagramassociation/add', DiagramAssociationEditView.as_view(), name='diagramassociation_add'),
    path('diagramassociation/edit', DiagramAssociationBulkEditView.as_view(), name='diagramassociation_bulk_edit'),
    path('diagramassociation/delete', DiagramAssociationBulkDeleteView.as_view(), name='diagramassociation_bulk_delete'),
    path('diagramassociation/<int:pk>/changelog', ObjectChangeLogView.as_view(), name='diagramassociation_changelog', kwargs={'model': DiagramAssociation}),
]
