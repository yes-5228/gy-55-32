from rest_framework.routers import DefaultRouter

from .views import ParcelViewSet


router = DefaultRouter()
router.register("", ParcelViewSet, basename="parcel")

urlpatterns = router.urls
