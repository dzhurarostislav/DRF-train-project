from django.contrib import admin
from .models import (
    Crew,
    Ticket,
    TrainType,
    Train,
    Station,
    Route,
    Journey,
    Order
)

admin.site.register(Crew)
admin.site.register(Ticket)
admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Journey)
admin.site.register(Order)

