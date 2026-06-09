import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("lockers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Parcel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tracking_no", models.CharField(max_length=50, unique=True)),
                ("sender_name", models.CharField(max_length=40)),
                ("receiver_name", models.CharField(max_length=40)),
                ("receiver_phone", models.CharField(max_length=30)),
                ("carrier", models.CharField(default="顺丰", max_length=40)),
                ("pickup_code", models.CharField(db_index=True, max_length=12)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("stored", "已入库"),
                            ("picked_up", "已取件"),
                            ("return_pending", "待退件"),
                            ("returned", "已退件"),
                        ],
                        default="stored",
                        max_length=20,
                    ),
                ),
                ("stored_at", models.DateTimeField(auto_now_add=True)),
                ("picked_up_at", models.DateTimeField(blank=True, null=True)),
                ("returned_at", models.DateTimeField(blank=True, null=True)),
                ("note", models.CharField(blank=True, max_length=200)),
                (
                    "locker_cell",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="parcels",
                        to="lockers.lockercell",
                    ),
                ),
            ],
            options={"ordering": ["-stored_at"]},
        ),
    ]
