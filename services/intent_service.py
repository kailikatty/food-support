def detect_intent(user_input):
    text = user_input.lower()

    if "delay" in text or "late" in text:
        return "delivery_delay"
    elif "wrong" in text:
        return "wrong_order"
    elif "quality" in text or "bad" in text:
        return "food_issue"
    elif "not receive" in text:
        return "not_received"
    elif "cancel" in text:
        return "cancel_order"

    return "general"