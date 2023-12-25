from django.urls import path, include
from rest_framework import routers

from train.views import (
    TrainTypeViewSet,
    TrainViewSet
)

router = routers.DefaultRouter()

router.register("train-types", TrainTypeViewSet)
router.register("train", TrainViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "train"
