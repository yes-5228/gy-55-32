from django.db import models


class Parcel(models.Model):
    class Status(models.TextChoices):
        STORED = "stored", "已入库"
        PICKED_UP = "picked_up", "已取件"
        RETURN_PENDING = "return_pending", "待退件"
        RETURNED = "returned", "已退件"

    tracking_no = models.CharField(max_length=50, unique=True)
    sender_name = models.CharField(max_length=40)
    receiver_name = models.CharField(max_length=40)
    receiver_phone = models.CharField(max_length=30)
    carrier = models.CharField(max_length=40, default="顺丰")
    locker_cell = models.ForeignKey(
        "lockers.LockerCell",
        on_delete=models.PROTECT,
        related_name="parcels",
    )
    pickup_code = models.CharField(max_length=12, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.STORED)
    stored_at = models.DateTimeField(auto_now_add=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-stored_at"]

    def __str__(self):
        return self.tracking_no
