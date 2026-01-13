from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from doctors.views import DoctorProfileViewSet, AvailabilitySlotViewSet
from appointments.views import AppointmentViewSet
from accounts import urls as accounts_urls

router = routers.DefaultRouter()
router.register(r"doctors", DoctorProfileViewSet, basename="doctorprofile")
router.register(r"availability", AvailabilitySlotViewSet, basename="availability")
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include((accounts_urls, "accounts"))),
    path("api/", include(router.urls)),
]