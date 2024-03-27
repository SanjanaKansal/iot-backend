from rest_framework_nested import routers

from datalogger.api import ElectricalLoggerViewSet, WaterLoggerViewSet

default_router = routers.SimpleRouter()

default_router.register("logElectricalData", ElectricalLoggerViewSet, basename="logElectricalData")
default_router.register("logWaterData", WaterLoggerViewSet, basename="logWaterData")
default_router.register("", ElectricalLoggerViewSet, basename="")

urlpatterns = default_router.urls
