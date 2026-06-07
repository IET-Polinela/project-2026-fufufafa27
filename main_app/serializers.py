from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    reporter_display = serializers.SerializerMethodField()  # ✅ TAMBAHAN LAB 12
    is_owner = serializers.SerializerMethodField()          # ✅ TAMBAHAN LAB 12

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description',
            'location', 'status', 'reporter',
            'reporter_display', 'is_owner',              # ✅ TAMBAHAN LAB 12
            'created_at', 'updated_at'
        ]

    def get_reporter(self, obj):
        return "Warga Anonim"

    # ✅ TAMBAHAN LAB 12 — tampilkan nama asli hanya ke pemilik laporan
    def get_reporter_display(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            if obj.reporter == request.user:
                return obj.reporter.username if obj.reporter else 'Warga Anonim'
        return 'Warga Anonim'

    # ✅ TAMBAHAN LAB 12 — cek apakah user adalah pemilik laporan
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user
        return False