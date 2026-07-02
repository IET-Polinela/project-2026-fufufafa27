from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    reporter_display = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()  # ✅ TAMBAHAN LAB 15
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description',
            'location', 'status', 'reporter',
            'reporter_display', 'reporter_name', 'is_owner',
            'created_at', 'updated_at'
        ]

    def get_reporter(self, obj):
        return "Warga Anonim"

    def get_reporter_display(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            if obj.reporter == request.user:
                return obj.reporter.username if obj.reporter else 'Warga Anonim'
        return 'Warga Anonim'

    def get_reporter_name(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            if obj.reporter == request.user:
                return obj.reporter.username if obj.reporter else 'Warga Anonim'
        return 'Warga Anonim'

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user
        return False