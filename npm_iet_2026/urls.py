from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),  # arahkan ke app
    path('contact/', include('contacts.urls')),  # arahkan ke app contact
    path('about/', include('about.urls')),  # arahkan ke app about
]