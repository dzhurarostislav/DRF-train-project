from rest_framework import serializers

from train.models import (
    TrainType,
    Train,
    Station,
    Route,
    Crew,
    Order,
    Ticket,
    Journey
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")
