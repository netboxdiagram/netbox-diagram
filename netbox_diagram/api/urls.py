from netbox.api.routers import NetBoxRouter

from .views import *

router = NetBoxRouter()
router.register("diagram", DiagramViewSet)
router.register("diagramassociation", DiagramAssociationViewSet)
urlpatterns = router.urls
