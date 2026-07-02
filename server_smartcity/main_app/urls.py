from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('report/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('add/', ReportCreateView.as_view(), name='report_create'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_update'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),  # ✅ TAMBAH
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
    path('api/search/', ReportSearchView.as_view(), name='report_search'),
    path('api/detail/<int:pk>/', ReportDetailApiView.as_view(), name='report_detail_api'),
]