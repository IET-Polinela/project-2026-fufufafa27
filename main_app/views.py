from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Report


# ✅ TAMBAHAN LAB 6 - Mixin proteksi Admin
class AdminRequiredMixin:
    """Hanya Admin yang boleh akses. Dicek di dispatch() sebelum view dieksekusi."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Kamu harus login terlebih dahulu.")
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak. Fitur ini hanya untuk Admin.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)


# ======================
# READ (LIST)
# ======================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'


# ======================
# DETAIL
# ======================
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'


# ======================
# CREATE
# ======================
class ReportCreateView(AdminRequiredMixin, CreateView):  # ✅ TAMBAHAN LAB 6
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan")
        return super().form_valid(form)


# ======================
# UPDATE
# ======================
class ReportUpdateView(AdminRequiredMixin, UpdateView):  # ✅ TAMBAHAN LAB 6
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
class ReportDeleteView(AdminRequiredMixin, DeleteView):  # ✅ TAMBAHAN LAB 6
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
class ReportUpdateStatusView(AdminRequiredMixin, View):  # ✅ TAMBAHAN LAB 6
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)

        new_status = request.POST.get('status')

        allowed_status = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']
        if new_status in allowed_status:
            report.status = new_status
            report.save()

            messages.success(request, "Status berhasil diperbarui")

        return redirect('report_list')