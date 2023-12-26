from rest_framework import viewsets

from train.models import TrainType, Train, Station, Route, Journey, Ticket, Order
from train.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    StationSerializer,
    RouteSerializer,
    RouteDetailSerializer,
    JourneyListSerializer,
    JourneyDetailSerializer, TicketSerializer, OrderSerializer,

)


class TrainTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TrainTypeSerializer
    queryset = TrainType.objects.all()


class TrainViewSet(viewsets.ModelViewSet):
    serializer_class = TrainSerializer
    queryset = Train.objects.select_related("train_type")


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer
    queryset = Station.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.select_related("source")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        return self.serializer_class


class JourneyViewSet(viewsets.ModelViewSet):
    serializer_class = JourneyListSerializer
    queryset = Journey.objects.select_related(
        "train__train_type",
        "route__source",
        "route__destination"
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return self.serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related("tickets__journey__train")

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
