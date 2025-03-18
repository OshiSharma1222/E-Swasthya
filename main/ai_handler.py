import google.generativeai as genai
import os
import json
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class AIHandler:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.error("Google API key not found in environment variables")
            raise ValueError("Google API key not found")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.system_prompt = """You are an AI Health Assistant for the E-Swasthya+ platform. Your role is to provide information about our healthcare services and features:

1. Medical Records Management:
   - Help users understand how to upload and manage medical reports
   - Explain the AI-powered report analysis feature
   - Guide users on viewing and organizing their health records

2. Family Health Dashboard:
   - Explain how to add and manage family members
   - Help track family members' health records
   - Provide guidance on family health monitoring

3. Emergency Services:
   - Guide users on using the SOS feature
   - Explain how to set up emergency contacts
   - Provide information about emergency response features

4. Hospital Finder:
   - Help users locate nearby hospitals
   - Explain how to use the hospital search feature
   - Provide guidance on emergency hospital services

5. Health Analysis:
   - Explain how our AI analyzes medical reports
   - Guide users on understanding health recommendations
   - Provide information about health tracking features

Important guidelines:
- Focus on explaining E-Swasthya+ features and services
- Provide clear step-by-step guidance when explaining features
- Maintain a helpful and professional tone
- Direct users to appropriate sections of the platform
- Recommend using emergency features when appropriate
"""

    def get_response(self, user_message, symptom_context=None):
        try:
            if not user_message:
                return {
                    'status': 'error',
                    'response': 'Empty message provided'
                }

            # Prepare the conversation
            conversation = self.model.start_chat(history=[])
            
            # Build the prompt
            prompt = f"{self.system_prompt}\n\n"
            
            if symptom_context and isinstance(symptom_context, dict):
                prompt += f"Context from symptom analysis:\n{json.dumps(symptom_context, indent=2)}\n\n"
                
            prompt += f"User question about E-Swasthya+: {user_message}\n\nProvide a helpful response focusing on our platform's features and services."
            
            # Get response from model
            response = conversation.send_message(prompt)
            
            if not response.text:
                logger.error("Empty response from AI model")
                return {
                    'status': 'error',
                    'response': 'Failed to generate response'
                }
                
            return {
                'status': 'success',
                'response': response.text
            }
            
        except Exception as e:
            logger.error(f"AI handler error: {str(e)}")
            return {
                'status': 'error',
                'response': f'Failed to process message: {str(e)}'
            }

# Initialize the AI handler
ai_handler = AIHandler() 