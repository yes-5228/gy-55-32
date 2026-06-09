from rest_framework import viewsets

from .models import PickupNotification
from .serializers import PickupNotificationSerializer


class PickupNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PickupNotification.objects.select_related("parcel").all()
    serializer_class = PickupNotificationSerializer
