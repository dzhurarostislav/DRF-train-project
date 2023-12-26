from django.shortcuts import render
from rest_framework import viewsets

from train.models import TrainType, Train, Station, Route
from train.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    StationSerializer,
    RouteSerializer,
    RouteDetailSerializer,

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
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RouteDetailSerializer
        return self.serializer_class
