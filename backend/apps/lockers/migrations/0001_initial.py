from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LockerCell",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=20, unique=True)),
                ("zone", models.CharField(default="A区", max_length=30)),
                (
                    "size",
                    models.CharField(
                        choices=[("small", "小"), ("medium", "中"), ("large", "大")],
                        default="medium",
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("empty", "空闲"), ("occupied", "已占用"), ("open", "已开门"), ("maintenance", "维护中")],
                        default="empty",
                        max_length=20,
                    ),
                ),
                ("temperature", models.DecimalField(decimal_places=2, default=24, max_digits=5)),
                ("last_opened_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["zone", "code"]},
        ),
    ]
