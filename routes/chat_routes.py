from flask import Blueprint, request, jsonify
from services.intent_service import detect_intent
from services.order_service import process_issue
from services.ai_service import generate_ai_response

user_state = {
    "food_issue": {
        "described": False,
        "image_uploaded": False
    }
}

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").lower()

    # 📸 detect image upload
    if "[image_uploaded]" in user_input:
        user_state["food_issue"]["image_uploaded"] = True
        intent = "food_issue"
    else:
        intent = detect_intent(user_input)

    follow_up_keywords = ["refund", "how", "when", "why", "where", "can i", "what"]
    is_follow_up = any(word in user_input for word in follow_up_keywords)

    # 🔥 OTHERS → AI
    if intent == "others" or intent == "unknown":
        reply = generate_ai_response(user_input, None)

    # 🔥 DELIVERY STAFF
    elif any(word in user_input for word in ["delivery man", "rider", "driver", "courier"]):
        reply = """We’re really sorry to hear about your experience with our delivery staff 🙏 
    That’s definitely not the level of service we aim to provide.
    We truly appreciate you bringing this to our attention. We will look into this matter and take appropriate action to prevent it from happening again.
    Please let us know if there’s anything else we can assist you with."""

    # 🔥 WRONG ORDER
    elif intent == "wrong_order":
        reply = (
            "We’re really sorry that you received the wrong order 🙏 That’s definitely not the experience we want for you.\n\n"
            "Could you please share a photo of your receipt or the items you received?"
            "This will help us verify the issue quickly.\n\n"
            "Once confirmed, we will process your refund right away."
        )

    # 🔥 FOOD ISSUE FLOW (แก้ตรงนี้สำคัญสุด)
    elif intent == "food_issue":

        # 🟡 user อธิบายปัญหา
        if any(word in user_input for word in ["insect", "spoiled", "bad", "cold"]):
            user_state["food_issue"]["described"] = True

        # 🟡 CASE 1: ส่งรูปก่อน ยังไม่อธิบาย
        if user_state["food_issue"]["image_uploaded"] and not user_state["food_issue"]["described"]:
            reply = (
                "Thank you for your photo 🙏\n\n"
                "Could you please describe what was wrong with the food?"
            )

        # 🟡 CASE 2: อธิบายแล้ว ยังไม่ส่งรูป
        elif user_state["food_issue"]["described"] and not user_state["food_issue"]["image_uploaded"]:
            reply = (
                "We're really sorry to hear that 🙏\n\n"
                "Please upload a photo so we can verify the issue."
            )

        # 🟡 CASE 3: ครบแล้ว → refund
        elif user_state["food_issue"]["described"] and user_state["food_issue"]["image_uploaded"]:
            reply = (
                "Thank you for your patience 🙏\n\n"
                "We have verified the issue and will proceed with your refund.\n"
                "We sincerely apologize for the inconvenience."
            )

            # ✅ reset state
            user_state["food_issue"] = {
                "described": False,
                "image_uploaded": False
            }

        # 🟡 CASE 4: เริ่มต้น
        else:
            reply = (
                "We're really sorry about your food issue 🙏\n\n"
                "Could you please describe what was wrong with the food?\n"
                "(e.g. cold, spoiled, missing items)\n\n"
                "You can also upload a photo for verification."
            )

    # 🔥 DELIVERY DELAY
    
    elif intent == "delivery_delay":
        reply = """We’re really sorry for the delay 🙏 We completely understand how frustrating this must be.
    Our team is currently checking your order status and will make sure this is resolved for you as soon as possible.
    💚 We’re here to help you every step of the way."""

    # 🔥 NOT RECEIVED
    elif intent == "not_received":
        reply = (
            "We’re really sorry you haven’t received your order 🙏 We understand how concerning this is.\n\n"
            "We’re checking your order right now, and if it hasn’t been delivered, we’ll make sure you receive a full refund 💚"
        )

    # 🔥 CANCEL ORDER
    elif intent == "cancel_order":
        reply = (
            "No worries at all 😊 Your order has been successfully cancelled.\n\n"
            "If you’ve already made a payment, the refund will be processed shortly. Let us know if you need anything else 💚"
        )

    # 🤖 FOLLOW-UP
    elif is_follow_up:
        reply = generate_ai_response(user_input, intent)

    # 🤖 DEFAULT
    else:
        reply = generate_ai_response(user_input, intent)

    return jsonify({
        "reply": reply,
        "intent": intent
    })
