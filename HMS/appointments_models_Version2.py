from django.db import models
from django.conf import settings

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("booked", "Booked"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("no-show", "No-Show"),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_appointments")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-start_time",)
        unique_together = ("doctor", "start_time", "end_time")

    def __str__(self):
        return f"Appointment {self.id} - {self.patient.username} with {self.doctor.username} at {self.start_time.isoformat()}"