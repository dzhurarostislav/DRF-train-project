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


class TrainSerializer(serializers.ModelSerializer):
    train_type = TrainTypeSerializer(many=False, read_only=True)
    train_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TrainType.objects.all(),
        write_only=True,
        source="train_type",
    )

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type",
            "train_type_id"
        )
