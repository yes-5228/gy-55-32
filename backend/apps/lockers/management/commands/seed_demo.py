from django.core.management.base import BaseCommand
from rest_framework.exceptions import ValidationError

from apps.lockers.models import LockerCell
from apps.parcels.services import inbound_parcel
from apps.parcels.models import Parcel


class Command(BaseCommand):
    help = "Create demo locker cells and parcels for local verification."

    def handle(self, *args, **options):
        cell_created = 0
        cell_skipped = 0
        parcel_created = 0
        parcel_skipped = 0
        parcel_failed = 0

        for zone in ["A区", "B区"]:
            for index in range(1, 13):
                size = (
                    LockerCell.Size.SMALL
                    if index <= 4
                    else LockerCell.Size.MEDIUM
                    if index <= 9
                    else LockerCell.Size.LARGE
                )
                _cell, created = LockerCell.objects.get_or_create(
                    code=f"{zone[0]}{index:02d}",
                    defaults={
                        "zone": zone,
                        "size": size,
                        "temperature": 23 + index / 10,
                    },
                )
                if created:
                    cell_created += 1
                else:
                    cell_skipped += 1

        if cell_created:
            self.stdout.write(
                self.style.SUCCESS(f"Created {cell_created} locker cells "
                                   f"(skipped {cell_skipped} existing).")
            )
        else:
            self.stdout.write(
                f"All {cell_created + cell_skipped} locker cells already exist, skipped."
            )

        samples = [
            {
                "tracking_no": "SF202606010001",
                "sender_name": "上海仓",
                "receiver_name": "张三",
                "receiver_phone": "13800000001",
                "carrier": "顺丰",
                "size": LockerCell.Size.SMALL,
                "note": "易碎",
            },
            {
                "tracking_no": "YD202606010002",
                "sender_name": "杭州仓",
                "receiver_name": "李四",
                "receiver_phone": "13800000002",
                "carrier": "韵达",
                "size": LockerCell.Size.MEDIUM,
                "note": "",
            },
            {
                "tracking_no": "ZT202606010003",
                "sender_name": "广州仓",
                "receiver_name": "王五",
                "receiver_phone": "13800000003",
                "carrier": "中通",
                "size": LockerCell.Size.LARGE,
                "note": "大件",
            },
        ]

        for sample in samples:
            tracking_no = sample["tracking_no"]
            if Parcel.objects.filter(tracking_no=tracking_no).exists():
                self.stdout.write(
                    f"  • Parcel {tracking_no} already exists, skipped."
                )
                parcel_skipped += 1
                continue
            try:
                inbound_parcel(sample.copy())
                parcel_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  • Inbound parcel {tracking_no}.")
                )
            except ValidationError as exc:
                parcel_failed += 1
                msg = "; ".join(
                    f"{k}: {', '.join(v) if isinstance(v, list) else v}"
                    for k, v in exc.detail.items()
                ) or str(exc)
                self.stdout.write(
                    self.style.WARNING(
                        f"  • Failed to create parcel {tracking_no}: {msg} (skipped)."
                    )
                )
            except Exception as exc:  # noqa: BLE001
                parcel_failed += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"  • Failed to create parcel {tracking_no}: {exc} (skipped)."
                    )
                )

        summary_parts = []
        if parcel_created:
            summary_parts.append(self.style.SUCCESS(f"created {parcel_created}"))
        if parcel_skipped:
            summary_parts.append(f"skipped {parcel_skipped}")
        if parcel_failed:
            summary_parts.append(self.style.WARNING(f"failed {parcel_failed}"))
        summary = (
            ", ".join(summary_parts) if summary_parts else "no changes"
        )
        self.stdout.write(self.style.SUCCESS(f"Demo data is ready ({summary})."))
