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
    train_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )
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


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    from_to = serializers.SerializerMethodField()
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(),
        write_only=True,
        source="source",
    )
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(),
        write_only=True,
        source="destination",
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "from_to",
            "source_id",
            "destination_id",
            "distance"
        )

    @staticmethod
    def get_from_to(obj) -> str:
        return str(obj)


class RouteDetailSerializer(serializers.ModelSerializer):
    source = StationSerializer(many=False, read_only=True)
    destination = StationSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class OrderSerializer(serializers.ModelSerializer):
    pass