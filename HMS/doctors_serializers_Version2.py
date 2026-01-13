from rest_framework import serializers
from .models import DoctorProfile, AvailabilitySlot
from accounts.serializers import UserSerializer
from accounts.models import User

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        fields = ("id", "user", "specialty", "license_no", "bio")

class AvailabilitySlotSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role="doctor"))
    class Meta:
        model = AvailabilitySlot
        fields = ("id", "doctor", "start_time", "end_time", "is_active")
        read_only_fields = ("id",)