from rest_framework.routers import DefaultRouter

from .views import PickupNotificationViewSet


router = DefaultRouter()
router.register("", PickupNotificationViewSet, basename="notification")

urlpatterns = router.urls
