from django.shortcuts import render
from rest_framework import viewsets

from train.models import TrainType
from train.serializers import TrainTypeSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TrainTypeSerializer
    queryset = TrainType.objects.all()
