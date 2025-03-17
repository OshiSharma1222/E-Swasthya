from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('report-analysis/<int:report_id>/', views.get_report_analysis, name='get_report_analysis'),
    path('trigger-emergency/', views.trigger_emergency, name='trigger_emergency'),
    path('emergency-contacts/', views.get_emergency_contacts, name='get_emergency_contacts'),
    path('emergency-contacts/add/', views.add_emergency_contact, name='add_emergency_contact'),
    path('emergency-contacts/<int:contact_id>/delete/', views.delete_emergency_contact, name='delete_emergency_contact'),
]