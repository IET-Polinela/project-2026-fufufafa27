from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.db.models import Count
from main_app.models import Report
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# ✅ TAMBAHAN LAB 15 - proteksi dashboard
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('login')
        if not request.user.is_admin:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


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
        return JsonResponse(data)