from rest_framework import serializers

from apps.lockers.models import LockerCell
from apps.lockers.serializers import LockerCellSerializer
from .models import Parcel


class ParcelSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    locker_cell_detail = LockerCellSerializer(source="locker_cell", read_only=True)

    class Meta:
        model = Parcel
        fields = [
            "id",
            "tracking_no",
            "sender_name",
            "receiver_name",
            "receiver_phone",
            "carrier",
            "locker_cell",
            "locker_cell_detail",
            "pickup_code",
            "status",
            "status_label",
            "stored_at",
            "picked_up_at",
            "returned_at",
            "note",
        ]
        read_only_fields = ["pickup_code", "status", "stored_at", "picked_up_at", "returned_at"]


class ParcelInboundSerializer(serializers.Serializer):
    tracking_no = serializers.CharField(max_length=50)
    sender_name = serializers.CharField(max_length=40)
    receiver_name = serializers.CharField(max_length=40)
    receiver_phone = serializers.CharField(max_length=30)
    carrier = serializers.CharField(max_length=40)
    size = serializers.ChoiceField(choices=LockerCell.Size.choices, required=False)
    note = serializers.CharField(max_length=200, required=False, allow_blank=True)


class PickupCodeSerializer(serializers.Serializer):
    pickup_code = serializers.CharField(max_length=12)


class PickupResultSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    parcel = ParcelSerializer(required=False)
