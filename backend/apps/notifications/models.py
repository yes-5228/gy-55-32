from django.db import models


class PickupNotification(models.Model):
    class Channel(models.TextChoices):
        SMS = "sms", "短信"
        WECHAT = "wechat", "微信"
        APP = "app", "App"

    class Status(models.TextChoices):
        SENT = "sent", "已发送"
        FAILED = "failed", "发送失败"

    parcel = models.ForeignKey(
        "parcels.Parcel",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.SMS)
    recipient = models.CharField(max_length=50)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SENT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_channel_display()} {self.recipient}"
