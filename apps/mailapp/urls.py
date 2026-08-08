from django.urls import path
from . import views

app_name = 'mailapp'

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('send/', views.send_email_view, name='send_email'),
    path('star/<int:mail_id>/', views.toggle_star_view, name='toggle_star'),
    path('delete/<int:mail_id>/', views.delete_email_view, name='delete_email'),
    path('home/', views.home_view, name='home'),
    path('campaigns/', views.campaigns_view, name='campaigns'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('integrations/', views.integrations_view, name='integrations'),
]
