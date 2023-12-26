from django.urls import path, include
from rest_framework import routers

from train.views import (
    TrainTypeViewSet,
    TrainViewSet,
    StationViewSet, RouteViewSet,
)

router = routers.DefaultRouter()

router.register("train-types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "train"
