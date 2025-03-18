from django.urls import path
from .views import (
    index, upload_report, get_report_analysis,
    process_chat,
    trigger_emergency, get_emergency_contacts,
    add_emergency_contact, delete_emergency_contact
)

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('upload-report/', upload_report, name='upload_report'),
    path('report-analysis/<int:report_id>/', get_report_analysis, name='get_report_analysis'),
    path('trigger-emergency/', trigger_emergency, name='trigger_emergency'),
    path('emergency-contacts/', get_emergency_contacts, name='get_emergency_contacts'),
    path('emergency-contacts/add/', add_emergency_contact, name='add_emergency_contact'),
    path('emergency-contacts/<int:contact_id>/delete/', delete_emergency_contact, name='delete_emergency_contact'),
    path('chat/process/', process_chat, name='process_chat'),
]