from django.db import models

from user.models import User


class Station(models.Model):
    name = models.CharField(max_length=63)
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
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="trains"
    )

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

    def __str__(self) -> str:
        return f"{self.journey}. Cargo: {self.cargo}, seat:{self.seat}"
