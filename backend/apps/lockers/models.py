from django.db import models


class LockerCell(models.Model):
    class Size(models.TextChoices):
        SMALL = "small", "小"
        MEDIUM = "medium", "中"
        LARGE = "large", "大"

    class Status(models.TextChoices):
        EMPTY = "empty", "空闲"
        OCCUPIED = "occupied", "已占用"
        OPEN = "open", "已开门"
        MAINTENANCE = "maintenance", "维护中"

    code = models.CharField(max_length=20, unique=True)
    zone = models.CharField(max_length=30, default="A区")
    size = models.CharField(max_length=20, choices=Size.choices, default=Size.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.EMPTY)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=24)
    last_opened_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["zone", "code"]

    def __str__(self):
        return f"{self.zone}-{self.code}"
