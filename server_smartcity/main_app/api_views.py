from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination  # ✅ TAMBAHAN LAB 12
from drf_spectacular.utils import extend_schema, extend_schema_view  # ✅ TAMBAHAN LAB 14
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly
from django.db.models import Q


# ✅ TAMBAHAN LAB 12 — Pagination
class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ✅ TAMBAHAN LAB 14 — OpenAPI schema documentation per action
@extend_schema_view(
    list=extend_schema(
        summary="Daftar semua laporan",
        description="Mengembalikan daftar laporan berdasarkan tab (my_reports / feed) dan paginasi.",
        tags=["Reports"],
    ),
    retrieve=extend_schema(
        summary="Detail laporan",
        description="Mengembalikan detail satu laporan berdasarkan ID.",
        tags=["Reports"],
    ),
    create=extend_schema(
        summary="Buat laporan baru",
        description="Membuat laporan baru. Reporter otomatis diset dari user yang login.",
        tags=["Reports"],
    ),
    update=extend_schema(
        summary="Update laporan (hanya DRAFT milik sendiri)",
        description="Hanya bisa dilakukan oleh pemilik laporan dan status masih DRAFT.",
        tags=["Reports"],
    ),
    partial_update=extend_schema(
        summary="Partial update laporan (hanya DRAFT milik sendiri)",
        tags=["Reports"],
    ),
    destroy=extend_schema(
        summary="Hapus laporan (hanya DRAFT milik sendiri)",
        description="Hanya bisa dilakukan oleh pemilik laporan dan status masih DRAFT.",
        tags=["Reports"],
        exclude=True,  # ✅ SKENARIO 1 LAB 14 — sembunyikan endpoint DELETE dari docs
    ),
)
class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination  # ✅ TAMBAHAN LAB 12

    def get_queryset(self):
        user = self.request.user

        # ✅ TAMBAHAN LAB 12 — Sorting terbaru
        queryset = Report.objects.all().order_by('-updated_at')

        # ✅ TAMBAHAN LAB 12 — Filtering berdasarkan tab
        tab = self.request.query_params.get('tab', None)

        if tab == 'my_reports':
            queryset = queryset.filter(reporter=user)
        elif tab == 'feed':
            queryset = queryset.filter(~Q(reporter=user) & ~Q(status='DRAFT'))
        else:
            # Default (sama seperti sebelumnya)
            if user.is_authenticated:
                queryset = queryset.filter(
                    Q(status__in=['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']) |
                    Q(status='DRAFT', reporter=user)
                )
            else:
                queryset = queryset.exclude(status='DRAFT')

        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)