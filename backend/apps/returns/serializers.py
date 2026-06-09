from rest_framework import serializers

from apps.parcels.serializers import ParcelSerializer
from .models import ReturnOrder


class ReturnOrderSerializer(serializers.ModelSerializer):
    reason_label = serializers.CharField(source="get_reason_display", read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    parcel_detail = ParcelSerializer(source="parcel", read_only=True)

    class Meta:
        model = ReturnOrder
        fields = [
            "id",
            "parcel",
            "parcel_detail",
            "reason",
            "reason_label",
            "operator",
            "status",
            "status_label",
            "remark",
            "created_at",
            "completed_at",
        ]
        read_only_fields = ["status", "created_at", "completed_at"]


class ReturnCreateSerializer(serializers.Serializer):
    parcel_id = serializers.IntegerField()
    reason = serializers.ChoiceField(choices=ReturnOrder.Reason.choices)
    operator = serializers.CharField(max_length=40)
    remark = serializers.CharField(max_length=200, required=False, allow_blank=True)
