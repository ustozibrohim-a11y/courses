"""
URL configuration. Admin panel is disabled.
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', include('courses.web_urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('courses.urls')),
]

if settings.DEBUG and settings.STATIC_URL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT or settings.BASE_DIR)
