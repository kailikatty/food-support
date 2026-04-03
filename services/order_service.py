orders = {
    "123": {"status": "on the way"},
}

def process_issue(intent):
    order_id = "123"
    status = orders.get(order_id, {}).get("status", "unknown")

    if intent == "delivery_delay":
        return f"Your order {order_id} is currently '{status}' 🚚"

    elif intent == "wrong_order":
        return f"Refund issued for order {order_id}."

    elif intent == "food_issue":
        return f"Refund issued for order {order_id}."

    elif intent == "not_received":
        if status != "delivered":
            return "Order not received. Refund processed."
        return "Order marked delivered. Investigating."

    elif intent == "cancel_order":
        orders[order_id]["status"] = "cancelled"
        return f"Order {order_id} cancelled."

    return None