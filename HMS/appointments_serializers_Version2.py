from rest_framework import serializers
from .models import Appointment
from accounts.serializers import UserSerializer
from django.utils import timezone
from doctors.models import AvailabilitySlot

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Appointment
        fields = ("id", "patient", "doctor", "start_time", "end_time", "status", "created_at")
        read_only_fields = ("id", "patient", "created_at", "status")

    def validate(self, attrs):
        start = attrs.get("start_time")
        end = attrs.get("end_time")
        doctor = attrs.get("doctor")
        if start >= end:
            raise serializers.ValidationError("start_time must be before end_time.")
        if start < timezone.now():
            raise serializers.ValidationError("Cannot book past times.")
        # Check that the chosen times fall into an active availability slot for doctor
        matched = AvailabilitySlot.objects.filter(
            doctor=doctor, is_active=True,
            start_time__lte=start, end_time__gte=end
        ).exists()
        if not matched:
            raise serializers.ValidationError("Selected time is not within doctor's availability.")
        # Also ensure no overlapping appointments for the doctor
        conflict = Appointment.objects.filter(doctor=doctor, start_time__lt=end, end_time__gt=start, status="booked").exists()
        if conflict:
            raise serializers.ValidationError("Doctor already has appointment in that time range.")
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["patient"] = request.user
        # status defaults to booked
        return super().create(validated_data)