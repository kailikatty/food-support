from flask import Blueprint, request, jsonify
from services.intent_service import detect_intent
from services.order_service import process_issue
from services.ai_service import generate_ai_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    intent = detect_intent(user_input)
    result = process_issue(intent)

    if result:
        reply = result
    else:
        reply = generate_ai_response(user_input)

    return jsonify({
        "reply": reply,
        "intent": intent
    })