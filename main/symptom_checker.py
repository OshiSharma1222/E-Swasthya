import google.generativeai as genai
import os
import json
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class SymptomChecker:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.error("Google API key not found in environment variables")
            raise ValueError("Google API key not found")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.system_prompt = """You are a medical symptom analysis AI. Your role is to:
1. Identify potential symptoms from user messages
2. Assess their severity (Low, Medium, High)
3. Suggest possible conditions
4. Recommend appropriate actions (self-care, doctor visit, emergency)

Format your response as a JSON with the following structure:
{
    "identified_symptoms": [{"symptom": "...", "severity": "..."}],
    "possible_conditions": ["condition1", "condition2"],
    "recommended_action": "...",
    "additional_notes": "..."
}

Important guidelines:
- Be thorough but conservative in your analysis
- Always recommend emergency care for severe symptoms
- Include clear disclaimers about seeking professional medical advice
- Do not make definitive diagnoses
"""

    def check_symptoms(self, user_message):
        try:
            if not user_message:
                return {
                    'status': 'error',
                    'message': 'Empty message provided'
                }

            # Prepare the conversation
            conversation = self.model.start_chat(history=[])
            conversation.send_message(f"{self.system_prompt}\n\nAnalyze this message: {user_message}")
            
            response = conversation.last.text
            
            try:
                # Try to parse the response as JSON
                analysis = json.loads(response)
                
                # Validate required fields
                required_fields = ['identified_symptoms', 'possible_conditions', 'recommended_action']
                if not all(field in analysis for field in required_fields):
                    logger.error(f"Missing required fields in analysis: {response}")
                    return {
                        'status': 'error',
                        'message': 'Invalid analysis format from AI'
                    }
                    
                return {
                    'status': 'success',
                    'analysis': analysis
                }
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {response}")
                return {
                    'status': 'error',
                    'message': 'Invalid response format from AI'
                }
                
        except Exception as e:
            logger.error(f"Symptom checker error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to analyze symptoms: {str(e)}'
            }

symptom_checker = SymptomChecker() 