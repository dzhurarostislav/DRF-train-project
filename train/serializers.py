from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
            "train_type_id",
            "image"
        )


class TrainImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "image")


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    from_to = serializers.CharField(source="__str__", read_only=True)
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


class JourneyListSerializer(serializers.ModelSerializer):
    route = serializers.CharField(source="route.__str__", read_only=True)
    train = serializers.CharField(source="train.name", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
    train_type = serializers.CharField(
        source="train.train_type.name", read_only=True
    )
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.select_related("source", "destination"),
        write_only=True,
        source="route",
    )
    train_id = serializers.PrimaryKeyRelatedField(
        queryset=Train.objects.select_related("train_type"),
        write_only=True,
        source="train",
    )
    departure_time = serializers.DateTimeField(
        read_only=False,
        format="%Y-%m-%d %H:%M"
    )
    arrival_time = serializers.DateTimeField(
        read_only=False,
        format="%Y-%m-%d %H:%M"
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "train_type",
            "departure_time",
            "arrival_time",
            "route_id",
            "train_id",
            "tickets_available",
        )


class JourneyDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer(many=False, read_only=True)
    train = TrainSerializer(many=False, read_only=True)
    crew = serializers.StringRelatedField(many=True, read_only=True)

    departure_time = serializers.DateTimeField(
        read_only=False,
        format="%Y-%m-%d %H:%M"
    )
    arrival_time = serializers.DateTimeField(
        read_only=False,
        format="%Y-%m-%d %H:%M"
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
            "arrival_time",
        )


class JourneyCrewSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField(many=False, read_only=True)
    departure_time = serializers.DateTimeField(
        read_only=False,
        format="%Y-%m-%d %H:%M"
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "departure_time"
        )


class CrewListSerializer(serializers.ModelSerializer):
    journeys = JourneyCrewSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
            "journeys"
        )


class CrewDetailSerializer(serializers.ModelSerializer):
    journeys = JourneyListSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
            "journeys"
        )


class TicketSerializer(serializers.ModelSerializer):
    journey = serializers.CharField(
        source="journey.route.__str__", read_only=True
    )
    journey_id = serializers.PrimaryKeyRelatedField(
        queryset=Journey.objects.select_related(
            "train__train_type",
            "route"
        ),
        write_only=True,
        source="journey",
    )
    departure_time = serializers.DateTimeField(
        source="journey.departure_time",
        read_only=True,
        format="%Y-%m-%d %H:%M"
    )

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["cargo"],
            attrs["seat"],
            attrs["journey"].train,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "cargo",
            "seat",
            "journey",
            "departure_time",
            "journey_id"
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    @transaction.atomic()
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)
        return order
