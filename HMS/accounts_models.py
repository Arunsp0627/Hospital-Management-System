from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_doctor(self):
        return self.role == "doctor"

    def is_patient(self):
        return self.role == "patient"