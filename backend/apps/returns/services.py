from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.lockers.models import LockerCell
from apps.parcels.models import Parcel
from .models import ReturnOrder


@transaction.atomic
def create_return_order(validated_data):
    parcel = (
        Parcel.objects.select_for_update()
        .select_related("locker_cell")
        .filter(id=validated_data["parcel_id"])
        .first()
    )
    if not parcel:
        raise ValidationError({"parcel_id": "快件不存在。"})
    if parcel.status != Parcel.Status.STORED:
        raise ValidationError({"parcel_id": "只有已入库且未取件的快件可发起退件。"})
    if hasattr(parcel, "return_order"):
        raise ValidationError({"parcel_id": "该快件已经存在退件单。"})

    parcel.status = Parcel.Status.RETURN_PENDING
    parcel.save(update_fields=["status"])
    return ReturnOrder.objects.create(
        parcel=parcel,
        reason=validated_data["reason"],
        operator=validated_data["operator"],
        remark=validated_data.get("remark", ""),
    )


@transaction.atomic
def complete_return_order(order):
    order = ReturnOrder.objects.select_for_update().select_related("parcel__locker_cell").get(id=order.id)
    if order.status != ReturnOrder.Status.PENDING:
        raise ValidationError({"status": "只有待处理退件单可完成。"})

    now = timezone.now()
    order.status = ReturnOrder.Status.COMPLETED
    order.completed_at = now
    order.save(update_fields=["status", "completed_at"])

    parcel = order.parcel
    parcel.status = Parcel.Status.RETURNED
    parcel.returned_at = now
    parcel.save(update_fields=["status", "returned_at"])

    cell = parcel.locker_cell
    cell.status = LockerCell.Status.EMPTY
    cell.last_opened_at = now
    cell.save(update_fields=["status", "last_opened_at", "updated_at"])
    return order
