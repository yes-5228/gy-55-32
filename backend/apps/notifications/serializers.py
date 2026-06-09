from rest_framework import serializers

from .models import PickupNotification


class PickupNotificationSerializer(serializers.ModelSerializer):
    channel_label = serializers.CharField(source="get_channel_display", read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    tracking_no = serializers.CharField(source="parcel.tracking_no", read_only=True)

    class Meta:
        model = PickupNotification
        fields = [
            "id",
            "parcel",
            "tracking_no",
            "channel",
            "channel_label",
            "recipient",
            "message",
            "status",
            "status_label",
            "created_at",
        ]
