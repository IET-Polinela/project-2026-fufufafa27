from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ LAB 10
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView       # ✅ LAB 14
from django_scalar.views import scalar_viewer                                       # ✅ LAB 14

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('contact/', include('contacts.urls')),
    path('about/', include('about.urls')),
    path('auth/', include('usermanagement_24782005.urls')),          # ✅ TAMBAHAN LAB 6
    path('dashboard/', include('dashboard_24782005.urls')),          # ✅ TAMBAHAN LAB 7
    path('api/', include('main_app.api_urls')),                      # ✅ TAMBAHAN LAB 9
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # ✅ LAB 10
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # ✅ LAB 10
    path('api/auth/', include('usermanagement_24782005.api_urls')),  # ✅ LAB 10

    # ✅ TAMBAHAN LAB 14 - OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),
]