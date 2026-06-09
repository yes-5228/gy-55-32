from rest_framework.routers import DefaultRouter

from .views import ReturnOrderViewSet


router = DefaultRouter()
router.register("", ReturnOrderViewSet, basename="return-order")

urlpatterns = router.urls
