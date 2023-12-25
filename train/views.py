from django.shortcuts import render
from rest_framework import viewsets

from train.models import TrainType, Train
from train.serializers import (
    TrainTypeSerializer,
    TrainSerializer,

)


class TrainTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TrainTypeSerializer
    queryset = TrainType.objects.all()


class TrainViewSet(viewsets.ModelViewSet):
    serializer_class = TrainSerializer
    queryset = Train.objects.select_related("train_type")
