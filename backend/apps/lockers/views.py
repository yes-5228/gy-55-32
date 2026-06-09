from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import LockerCell
from .serializers import LockerCellSerializer


class LockerCellViewSet(viewsets.ModelViewSet):
    queryset = LockerCell.objects.all()
    serializer_class = LockerCellSerializer

    @action(detail=False, methods=["get"])
    def summary(self, request):
        total = LockerCell.objects.count()
        by_status = {
            item["status"]: item["count"]
            for item in LockerCell.objects.values("status").annotate(count=Count("id"))
        }
        return Response(
            {
                "total": total,
                "empty": by_status.get(LockerCell.Status.EMPTY, 0),
                "occupied": by_status.get(LockerCell.Status.OCCUPIED, 0),
                "open": by_status.get(LockerCell.Status.OPEN, 0),
                "maintenance": by_status.get(LockerCell.Status.MAINTENANCE, 0),
            }
        )

    @action(detail=True, methods=["post"])
    def mark_maintenance(self, request, pk=None):
        cell = self.get_object()
        cell.status = LockerCell.Status.MAINTENANCE
        cell.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(cell).data)

    @action(detail=True, methods=["post"])
    def reset(self, request, pk=None):
        cell = self.get_object()
        cell.status = LockerCell.Status.EMPTY
        cell.last_opened_at = timezone.now()
        cell.save(update_fields=["status", "last_opened_at", "updated_at"])
        return Response(self.get_serializer(cell).data)
