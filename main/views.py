from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MedicalReport, ReportAnalysis, EmergencyContact, EmergencyAlert
from .ai_analysis import analyze_medical_report
import os
from datetime import datetime
import json
import requests
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def index(request):
    return render(request, 'main/index.html')

@csrf_exempt
def upload_report(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('report')
            if not file:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No file uploaded'
                }, status=400)

            # Generate a unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = os.path.splitext(file.name)[1].lower()
            filename = f'reports/{timestamp}{file_extension}'
            
            # Save the file using default_storage
            file_path = default_storage.save(filename, ContentFile(file.read()))
            
            # Create report object
            report = MedicalReport.objects.create(
                title=f"Report_{timestamp}",
                report_type='pdf' if file_extension == '.pdf' else 'image',
                file=file_path
            )
            
            # Get the full file path
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Analyze the report using AI
            analysis_result = analyze_medical_report(full_file_path)
            
            # Create analysis object
            analysis = ReportAnalysis.objects.create(
                report=report,
                analysis_text=analysis_result['analysis_text'],
                health_tips=analysis_result['health_tips'],
                yoga_suggestions=analysis_result['yoga_suggestions']
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Report uploaded and analyzed successfully',
                'report_id': report.id,
                'file_url': report.file.url if report.file else None,
                'analysis': {
                    'text': analysis.analysis_text,
                    'health_tips': analysis.health_tips,
                    'yoga_suggestions': analysis.yoga_suggestions
                }
            })
            
        except Exception as e:
            # Clean up the uploaded file if analysis fails
            if 'file_path' in locals():
                default_storage.delete(file_path)
            
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def get_report_analysis(request, report_id):
    try:
        report = MedicalReport.objects.get(id=report_id)
        analysis = ReportAnalysis.objects.get(report=report)
        
        return JsonResponse({
            'status': 'success',
            'analysis': {
                'text': analysis.analysis_text,
                'health_tips': analysis.health_tips,
                'yoga_suggestions': analysis.yoga_suggestions
            }
        })
    except MedicalReport.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Report not found'
        }, status=404)
    except ReportAnalysis.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Analysis not found'
        }, status=404)

@csrf_exempt
def trigger_emergency(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alert_type = data.get('type')
            location = data.get('location')
            message = data.get('message', '')
            
            # Create emergency alert
            alert = EmergencyAlert.objects.create(
                alert_type=alert_type,
                location=location,
                message=message
            )
            
            # Handle different alert types
            if alert_type == 'ambulance':
                # In a real application, this would integrate with an ambulance service API
                alert.status = 'completed'
                alert.message = 'Ambulance has been called and is on the way.'
                alert.save()
                
            elif alert_type == 'family':
                # In a real application, this would send SMS/email to family members
                alert.status = 'completed'
                alert.message = 'Family members have been notified.'
                alert.save()
                
            elif alert_type == 'location':
                # In a real application, this would share location via SMS/email
                alert.status = 'completed'
                alert.message = 'Location has been shared with emergency contacts.'
                alert.save()
            
            return JsonResponse({
                'status': 'success',
                'message': alert.message,
                'alert_id': alert.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@csrf_exempt
def add_emergency_contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contact = EmergencyContact.objects.create(
                name=data.get('name'),
                phone=data.get('phone'),
                relationship=data.get('relationship')
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Contact added successfully',
                'contact': {
                    'id': contact.id,
                    'name': contact.name,
                    'phone': contact.phone,
                    'relationship': contact.relationship
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def get_emergency_contacts(request):
    contacts = EmergencyContact.objects.all()
    contacts_list = [{
        'id': contact.id,
        'name': contact.name,
        'phone': contact.phone,
        'relationship': contact.relationship
    } for contact in contacts]
    return JsonResponse({
        'status': 'success',
        'contacts': contacts_list
    })

@csrf_exempt
def delete_emergency_contact(request, contact_id):
    if request.method == 'DELETE':
        try:
            contact = EmergencyContact.objects.get(id=contact_id)
            contact.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Contact deleted successfully'
            })
        except EmergencyContact.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Contact not found'
            }, status=404)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405) 