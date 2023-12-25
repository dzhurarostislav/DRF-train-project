from django.urls import path, include
from rest_framework import routers

from train.views import TrainTypeViewSet

router = routers.DefaultRouter()

router.register("train-types", TrainTypeViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "train"
