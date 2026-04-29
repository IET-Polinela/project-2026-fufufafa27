from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('contact/', include('contacts.urls')),
    path('about/', include('about.urls')),
    path('auth/', include('usermanagement_24782005.urls')),  # ✅ TAMBAHAN LAB 6
    path('dashboard/', include('dashboard_24782005.urls')),  # ✅ TAMBAHAN LAB 7
]