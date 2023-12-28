import os
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from user.models import User


class Station(models.Model):
    name = models.CharField(max_length=63, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.source} - {self.destination}"


class TrainType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/trains/", filename)


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="trains"
    )
    image = models.ImageField(null=True, upload_to=movie_image_file_path)

    def __str__(self) -> str:
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="users"
    )

    def __str__(self) -> str:
        return f"Order №{self.id}, created_at: {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Journey(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="journeys"
    )
    train = models.ForeignKey(
        Train, on_delete=models.CASCADE, related_name="journeys"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys")

    def __str__(self) -> str:
        return f"{self.route} departure time: {self.departure_time}"


class Ticket(models.Model):
    cargo = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_ticket(cargo, seat, train, error_to_raise):
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (cargo, "cargo", "cargo_num"),
            (seat, "seat", "places_in_cargo"),
        ]:
            count_attrs = getattr(train, train_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {train_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.cargo,
            self.seat,
            self.journey.train,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{self.journey}. Cargo: {self.cargo}, seat:{self.seat}"

    class Meta:
        unique_together = ("journey", "cargo", "seat")
        ordering = ["cargo", "seat"]
