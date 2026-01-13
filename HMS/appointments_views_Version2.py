from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.exceptions import PermissionDenied

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "patient"

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("patient", "doctor").all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor():
            # doctors see only their appointments
            return Appointment.objects.filter(doctor=user)
        if user.is_patient():
            return Appointment.objects.filter(patient=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_patient():
            raise PermissionDenied("Only patients can create appointments.")
        serializer.save()
    
    def perform_update(self, serializer):
        # Patients should not change doctor; doctors can update status etc for their appointments
        obj = self.get_object()
        user = self.request.user
        if user.is_patient() and obj.patient != user:
            raise PermissionDenied("Patients can only modify their own appointments.")
        if user.is_doctor() and obj.doctor != user:
            raise PermissionDenied("Doctors can only modify their own appointments.")
        serializer.save()