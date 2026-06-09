from django.db import models


class ReturnOrder(models.Model):
    class Reason(models.TextChoices):
        TIMEOUT = "timeout", "逾期未取"
        REJECTED = "rejected", "用户拒收"
        DAMAGED = "damaged", "快件破损"
        OTHER = "other", "其他"

    class Status(models.TextChoices):
        PENDING = "pending", "待处理"
        COMPLETED = "completed", "已退回"
        CANCELLED = "cancelled", "已取消"

    parcel = models.OneToOneField(
        "parcels.Parcel",
        on_delete=models.CASCADE,
        related_name="return_order",
    )
    reason = models.CharField(max_length=20, choices=Reason.choices, default=Reason.TIMEOUT)
    operator = models.CharField(max_length=40, default="管理员")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    remark = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"退件 {self.parcel.tracking_no}"
