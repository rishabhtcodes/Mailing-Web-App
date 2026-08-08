from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static
from apps.mailapp.views import landing_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('mail/', include('apps.mailapp.urls')),
    path('', landing_view, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

