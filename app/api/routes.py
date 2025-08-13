from flask import Blueprint, request, jsonify
import openai
from flask import current_app
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Check for API key first
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return jsonify({
                'response': 'Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable.'
            })
            
        try:
            # For OpenAI v0.28.0
            import openai
            
            # Set the API key
            openai.api_key = api_key
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a student check-in system. Keep responses concise and helpful."},
                    {"role": "user", "content": user_message}
                ]
            )
            
            return jsonify({
                'response': response.choices[0].message['content'].strip()
            })
            
        except Exception as e:
            current_app.logger.error(f"Error in OpenAI API call: {str(e)}")
            return jsonify({
                'response': f"I'm sorry, I encountered an error: {str(e)}"
            }), 500
        
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': f"I'm sorry, I encountered an error: {str(e)}"
        }), 500
