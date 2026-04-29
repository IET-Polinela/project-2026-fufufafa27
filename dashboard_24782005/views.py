from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.db.models import Count
from main_app.models import Report


# ======================
# HALAMAN UTAMA DASHBOARD
# ======================
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'


# ======================
# API: DATA STATISTIK (untuk Chart.js)
# ======================
class DashboardStatsView(View):
    def get(self, request):
        status_data = (
            Report.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        category_data = (
            Report.objects
            .values('category')
            .annotate(count=Count('id'))
            .order_by('category')
        )
        latest_reported = list(
            Report.objects
            .filter(status='REPORTED')
            .order_by('-created_at')[:5]
            .values('id', 'title', 'category', 'location', 'status', 'created_at')
        )
        latest_resolved = list(
            Report.objects
            .filter(status='RESOLVED')
            .order_by('-created_at')[:5]
            .values('id', 'title', 'category', 'location', 'status', 'created_at')
        )
        for item in latest_reported + latest_resolved:
            item['created_at'] = item['created_at'].strftime('%d %b %Y') if item['created_at'] else '-'

        data = {
            'status': list(status_data),
            'category': list(category_data),
            'latest_reported': latest_reported,
            'latest_resolved': latest_resolved,
        }
        print("[DashboardStats] Data dikirim:", data)
        return JsonResponse(data)