from flask import Blueprint, jsonify, request

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/start', methods=['POST'])
def start_chat():
    data = request.get_json()
    # Process the chat input, e.g., "No results found." trigger
    # Here we apply rule-based logic and return the next step in conversation.
    response = {
        "message": "Looks like there aren’t any properties matching your search. Would you like us to conduct a deeper search on the web?",
        "options": ["Yes, please!", "No, thanks."]
    }
    return jsonify(response)
