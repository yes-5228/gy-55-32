import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("parcels", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PickupNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "channel",
                    models.CharField(choices=[("sms", "短信"), ("wechat", "微信"), ("app", "App")], default="sms", max_length=20),
                ),
                ("recipient", models.CharField(max_length=50)),
                ("message", models.TextField()),
                ("status", models.CharField(choices=[("sent", "已发送"), ("failed", "发送失败")], default="sent", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "parcel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to="parcels.parcel",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
