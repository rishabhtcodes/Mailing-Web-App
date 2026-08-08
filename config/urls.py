from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.shortcuts import redirect

def root_redirect(request):
    return redirect('mailapp:inbox')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('mail/', include('apps.mailapp.urls')),
    path('', root_redirect, name='index'),
]
