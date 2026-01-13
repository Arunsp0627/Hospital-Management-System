from rest_framework import viewsets, permissions
from .models import DoctorProfile, AvailabilitySlot
from .serializers import DoctorProfileSerializer, AvailabilitySlotSerializer
from rest_framework.exceptions import PermissionDenied

class IsDoctorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "doctor"

class DoctorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorProfile.objects.select_related("user").all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class AvailabilitySlotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilitySlot.objects.all()
    serializer_class = AvailabilitySlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor():
            # Doctors only see their own slots when authenticated
            return AvailabilitySlot.objects.filter(doctor=user)
        # Patients can view all active slots
        return AvailabilitySlot.objects.filter(is_active=True)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_doctor():
            raise PermissionDenied("Only doctors can create availability slots.")
        # Force doctor to be request.user
        serializer.save(doctor=user)
    
    def perform_update(self, serializer):
        user = self.request.user
        obj = self.get_object()
        if obj.doctor != user:
            raise PermissionDenied("Cannot modify another doctor's slots.")
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        if instance.doctor != user:
            raise PermissionDenied("Cannot delete another doctor's slots.")
        instance.delete()