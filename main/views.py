from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MedicalReport, ReportAnalysis, EmergencyContact, EmergencyAlert
import os
from datetime import datetime
import json
import requests
from django.conf import settings

def index(request):
    return render(request, 'main/index.html')

@csrf_exempt  # Temporarily disable CSRF protection for testing
def upload_report(request):
    if request.method == 'POST':
        try:
            file = request.FILES.get('report')
            title = request.POST.get('title', f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Determine file type
            file_extension = os.path.splitext(file.name)[1].lower()
            report_type = 'pdf' if file_extension == '.pdf' else 'image'
            
            # Create report object
            report = MedicalReport.objects.create(
                title=title,
                report_type=report_type,
                file=file
            )
            
            # For demo purposes, create a sample analysis
            analysis = ReportAnalysis.objects.create(
                report=report,
                analysis_text="Based on your medical report, here's what we found:\n\n1. Your overall health indicators are within normal range\n2. Blood pressure and heart rate are stable\n3. No significant abnormalities detected",
                health_tips="1. Maintain a balanced diet with plenty of fruits and vegetables\n2. Exercise regularly (30 minutes daily)\n3. Get 7-8 hours of sleep each night\n4. Stay hydrated (8 glasses of water daily)\n5. Practice stress management techniques",
                yoga_suggestions="1. Start with Surya Namaskar (Sun Salutation) - 5 rounds daily\n2. Practice Pranayama (Breathing exercises) - 10 minutes\n3. Include gentle stretches in your morning routine\n4. Try meditation for 15 minutes daily\n5. End your day with relaxation poses"
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Report uploaded and analyzed successfully',
                'report_id': report.id,
                'analysis': {
                    'text': analysis.analysis_text,
                    'health_tips': analysis.health_tips,
                    'yoga_suggestions': analysis.yoga_suggestions
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