import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("parcels", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReturnOrder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "reason",
                    models.CharField(
                        choices=[("timeout", "逾期未取"), ("rejected", "用户拒收"), ("damaged", "快件破损"), ("other", "其他")],
                        default="timeout",
                        max_length=20,
                    ),
                ),
                ("operator", models.CharField(default="管理员", max_length=40)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "待处理"), ("completed", "已退回"), ("cancelled", "已取消")],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("remark", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "parcel",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="return_order",
                        to="parcels.parcel",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
