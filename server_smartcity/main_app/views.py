from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Report


# ✅ Mixin proteksi Admin
class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Kamu harus login terlebih dahulu.")
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak. Fitur ini hanya untuk Admin.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)


# ✅ Mixin proteksi Login
class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Kamu harus login terlebih dahulu.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


# ======================
# HOME
# ======================
class HomeView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports_reported']    = Report.objects.filter(status='REPORTED').count()
        context['reports_in_progress'] = Report.objects.filter(status='IN_PROGRESS').count()
        context['reports_resolved']    = Report.objects.filter(status='RESOLVED').count()
        return context


# ======================
# READ (LIST) - ✅ UBAH: tambah AdminRequiredMixin
# ======================
class ReportListView(AdminRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_admin:
            return Report.objects.all().order_by('-created_at')
        else:
            return Report.objects.exclude(status='DRAFT').order_by('-created_at')


# ======================
# DETAIL - ✅ UBAH: tambah AdminRequiredMixin
# ======================
class ReportDetailView(AdminRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'


# ======================
# CREATE - ✅ UBAH: tambah AdminRequiredMixin
# ======================
class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.status = 'REPORTED'
        messages.success(self.request, "Laporan berhasil ditambahkan")
        return super().form_valid(form)


# ======================
# UPDATE
# ======================
class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui")
        return super().form_valid(form)


# ======================
# DELETE
# ======================
class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')
    context_object_name = 'report'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan berhasil dihapus")
        return super().delete(request, *args, **kwargs)


# ======================
# WORKFLOW STATUS
# ======================
class ReportUpdateStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        allowed_status = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']
        if new_status in allowed_status:
            report.status = new_status
            report.save()
            messages.success(request, "Status berhasil diperbarui")
        return redirect('report_list')


# ✅ Live Search - tambah AdminRequiredMixin
class ReportSearchView(AdminRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        reports = Report.objects.all()
        if query:
            reports = reports.filter(title__icontains=query)
        data = list(
            reports.order_by('-created_at')[:20]
            .values('id', 'title', 'category', 'location', 'status', 'created_at')
        )
        for item in data:
            item['created_at'] = item['created_at'].strftime('%d %b %Y') if item['created_at'] else '-'
        return JsonResponse({'reports': data})


# ✅ Detail Modal API
class ReportDetailApiView(View):
    def get(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
            data = {
                'id': report.id,
                'title': report.title,
                'category': report.category,
                'description': report.description,
                'location': report.location,
                'status': report.status,
                'created_at': report.created_at.strftime('%d %b %Y %H:%M') if report.created_at else '-',
            }
            return JsonResponse(data)
        except Report.DoesNotExist:
            return JsonResponse({'error': 'Laporan tidak ditemukan'}, status=404)


# ✅ TAMBAHAN LAB 15 - fungsi untuk test_addtional.py
def report_detail_api(request, pk):
    report = get_object_or_404(Report, pk=pk)
    data = {
        'id': report.id,
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
        'created_at': report.created_at.strftime('%d %b %Y %H:%M') if report.created_at else '-',
    }
    return JsonResponse(data)