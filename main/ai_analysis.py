import os

def analyze_medical_report(file_path):
    """
    Provide static analysis results for medical reports
    """
    try:
        # Static analysis results
        analysis_text = """Analysis Results:

1. Your overall health indicators are within normal range
2. Blood pressure and heart rate are stable
3. No significant abnormalities detected"""

        health_tips = """1. Maintain a balanced diet with plenty of fruits and vegetables
2. Exercise regularly (30 minutes daily)
3. Get 7-8 hours of sleep each night
4. Stay hydrated (8 glasses of water daily)
5. Practice stress management techniques"""

        yoga_suggestions = """1. Start with Surya Namaskar (Sun Salutation) - 5 rounds daily
2. Practice Pranayama (Breathing exercises) - 10 minutes
3. Include gentle stretches in your morning routine
4. Try meditation for 15 minutes daily
5. End your day with relaxation poses"""

        return {
            'analysis_text': analysis_text,
            'health_tips': health_tips,
            'yoga_suggestions': yoga_suggestions
        }
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        return {
            'analysis_text': "Error analyzing the report. Please try again.",
            'health_tips': "Unable to generate health tips at this time.",
            'yoga_suggestions': "Unable to generate yoga suggestions at this time."
        } 