"""dataskipper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers

from dashboard.api import (
    DashboardViewSet,
    EnergyDashboardViewSet,
    PowerDashboardViewSet,
    WaterFlowDashboardViewSet,
    WaterVolumeDashboardViewSet,
)
from datalogger.api import (
    ClientDashboardViewSet,
    ElectricalLoggerViewSet,
    HealthcheckViewSet,
    LoggerViewSet,
    WaterLoggerViewSet,
    TagViewSet
)
from user.api import (
    UserLoginViewSet,
    UserLogoutViewSet,
    UserRegisterViewSet,
    VerifyEmailViewSet,
)

default_router = routers.SimpleRouter()
default_router.register(
    "healthcheck", HealthcheckViewSet, basename="healthcheck"
)
default_router.register(
    "populateDummyData", LoggerViewSet, basename="populateDummyData"
)
default_router.register(
    "logElectricalData", ElectricalLoggerViewSet, basename="logElectricalData"
)
default_router.register("logWaterData", WaterLoggerViewSet, basename="logWaterData")
default_router.register(
    "powerHistogram", PowerDashboardViewSet, basename="powerHistogram"
)
default_router.register(
    "energyHistogram", EnergyDashboardViewSet, basename="energyHistogram"
)
default_router.register(
    "waterFlowHistogram", WaterFlowDashboardViewSet, basename="waterFlowHistogram"
)
default_router.register(
    "waterVolumeHistogram", WaterVolumeDashboardViewSet, basename="waterVolumeHistogram"
)
default_router.register("allClients", ClientDashboardViewSet, basename="allClients")
default_router.register("registerUser", UserRegisterViewSet, basename="registerUser")
default_router.register("loginUser", UserLoginViewSet, basename="loginUser")
default_router.register("logoutUser", UserLogoutViewSet, basename="logoutUser")
default_router.register("accountVerify", VerifyEmailViewSet, basename="accountVerify")

default_router.register("dashboard", DashboardViewSet, basename="dashboard")
default_router.register("tag", TagViewSet, basename="tag")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("iot-backend/api/v1/", include(default_router.urls)),
    path("silk/", include("silk.urls", namespace="silk")),
]
