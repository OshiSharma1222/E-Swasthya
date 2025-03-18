from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import EmergencyContact, EmergencyAlert

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
                alert.status = 'completed'
                alert.message = 'Ambulance has been called and is on the way.'
                alert.save()
                
            elif alert_type == 'family':
                alert.status = 'completed'
                alert.message = 'Family members have been notified.'
                alert.save()
                
            elif alert_type == 'location':
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