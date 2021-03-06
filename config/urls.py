"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    # path(settings.ADMIN_URL, admin.site.urls),

    path('', include(('apps.companies.urls', 'companies'), namespace='companies')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
