from flask import Blueprint, request, jsonify
from services.intent_service import detect_intent
from services.order_service import process_issue
from services.ai_service import generate_ai_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").lower()

    intent = detect_intent(user_input)

    # 🧠 detect follow-up (สำคัญมาก)
    follow_up_keywords = ["refund", "how", "when", "why", "where", "can i", "what"]

    is_follow_up = any(word in user_input for word in follow_up_keywords)

    # ✅ ถ้าเป็น follow-up → ให้ AI ตอบเลย
    if is_follow_up:
        reply = generate_ai_response(user_input, intent)

    # 🧠 rule-based (เฉพาะเคสหลัก)
    elif intent == "delivery_delay":
        reply = "Your order 001 is still on the way. It should arrive shortly. If the delay continues, we can offer a discount for your next order."

    elif intent == "wrong_order":
        reply = "A refund has been issued for order 001. It will be processed within a few business days."

    elif intent == "food_issue":
        reply = "We have issued a refund for order 001 due to the food quality issue."

    elif intent == "not_received":
        reply = "We’re checking your order now. If it was not delivered, you will receive a full refund."

    elif intent == "cancel_order":
        reply = "Your order has been cancelled. If payment was completed, the refund will be processed shortly."

    # 🤖 default → AI
    else:
        reply = generate_ai_response(user_input, intent)

    return jsonify({
        "reply": reply,
        "intent": intent
    })
    
