from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly
from django.db.models import Q


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Tampilkan semua non-DRAFT + DRAFT milik user sendiri
            return Report.objects.filter(
                Q(status__in=['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']) |
                Q(status='DRAFT', reporter=user)
            )
        return Report.objects.exclude(status='DRAFT')

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)