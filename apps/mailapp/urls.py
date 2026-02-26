from django.urls import path
from . import views

app_name = 'mailapp'

urlpatterns = [
    path('send/', views.send_email_view, name='send_email'),
    path('history/', views.email_history_view, name='email_history'),
]
