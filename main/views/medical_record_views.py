from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ..services.blockchain_service import BlockchainService
import hashlib

blockchain_service = BlockchainService()

def generate_report_hash(patient_id, report_data):
    """Generate a unique hash for the medical report"""
    data = f"{patient_id}-{report_data}".encode()
    return hashlib.sha256(data).hexdigest()

@csrf_exempt
@require_http_methods(["POST"])
def store_medical_record(request):
    """Store a new medical record on the blockchain"""
    try:
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        report_data = data.get('report_data')
        
        if not patient_id or not report_data:
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields'
            }, status=400)
        
        # Generate report hash
        report_hash = generate_report_hash(patient_id, report_data)
        
        # Store on blockchain
        result = blockchain_service.store_medical_record(
            patient_id,
            report_hash,
            report_data
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_medical_record(request, patient_id, report_hash):
    """Retrieve a medical record from the blockchain"""
    try:
        result = blockchain_service.get_medical_record(patient_id, report_hash)
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=404)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_medical_record(request, patient_id, report_hash):
    """Update an existing medical record"""
    try:
        data = json.loads(request.body)
        new_report_data = data.get('report_data')
        
        if not new_report_data:
            return JsonResponse({
                'success': False,
                'error': 'Missing report data'
            }, status=400)
        
        result = blockchain_service.update_medical_record(
            patient_id,
            report_hash,
            new_report_data
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def invalidate_medical_record(request, patient_id, report_hash):
    """Invalidate a medical record"""
    try:
        result = blockchain_service.invalidate_medical_record(
            patient_id,
            report_hash
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def verify_record_integrity(request, patient_id, report_hash):
    """Verify the integrity of a medical record"""
    try:
        result = blockchain_service.verify_record_integrity(
            patient_id,
            report_hash
        )
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500) 