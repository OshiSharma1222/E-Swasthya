from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from ..models import MedicalReport, ReportAnalysis
from ..ai_analysis import analyze_medical_report
import os
from datetime import datetime
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