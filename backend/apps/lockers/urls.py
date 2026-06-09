from rest_framework.routers import DefaultRouter

from .views import LockerCellViewSet


router = DefaultRouter()
router.register("cells", LockerCellViewSet, basename="locker-cell")

urlpatterns = router.urls
