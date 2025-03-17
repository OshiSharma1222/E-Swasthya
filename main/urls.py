from django.urls import path
from . import views
from .views import medical_record_views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('report-analysis/<int:report_id>/', views.get_report_analysis, name='get_report_analysis'),
    path('trigger-emergency/', views.trigger_emergency, name='trigger_emergency'),
    path('emergency-contacts/', views.get_emergency_contacts, name='get_emergency_contacts'),
    path('emergency-contacts/add/', views.add_emergency_contact, name='add_emergency_contact'),
    path('emergency-contacts/<int:contact_id>/delete/', views.delete_emergency_contact, name='delete_emergency_contact'),
    # Medical Record Blockchain endpoints
    path('api/medical-records/', medical_record_views.store_medical_record, name='store_medical_record'),
    path('api/medical-records/<str:patient_id>/<str:report_hash>/', medical_record_views.get_medical_record, name='get_medical_record'),
    path('api/medical-records/<str:patient_id>/<str:report_hash>/update/', medical_record_views.update_medical_record, name='update_medical_record'),
    path('api/medical-records/<str:patient_id>/<str:report_hash>/invalidate/', medical_record_views.invalidate_medical_record, name='invalidate_medical_record'),
    path('api/medical-records/<str:patient_id>/<str:report_hash>/verify/', medical_record_views.verify_record_integrity, name='verify_record_integrity'),
]