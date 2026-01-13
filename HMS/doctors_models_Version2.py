from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=200, blank=True)
    license_no = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="availability_slots")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("start_time",)
        unique_together = ("doctor", "start_time", "end_time")

    def __str__(self):
        return f"{self.doctor.username}: {self.start_time.isoformat()} -> {self.end_time.isoformat()}"