from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ReturnOrder
from .serializers import ReturnCreateSerializer, ReturnOrderSerializer
from .services import complete_return_order, create_return_order


class ReturnOrderViewSet(viewsets.ModelViewSet):
    queryset = ReturnOrder.objects.select_related("parcel", "parcel__locker_cell").all()
    serializer_class = ReturnOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = ReturnCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = create_return_order(serializer.validated_data)
        return Response(ReturnOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        order = complete_return_order(self.get_object())
        return Response(ReturnOrderSerializer(order).data)
