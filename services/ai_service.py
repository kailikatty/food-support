import os
from google import genai

# ✅ init client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ✅ FIX: ต้องประกาศก่อนใช้
chat_history = []

def generate_ai_response(user_input, intent=None):
    global chat_history

    try:
        # ✅ limit history กันยาวเกิน
        history = "\n".join(chat_history[-6:])

        prompt = f"""
        You are a professional food delivery support agent.

        Rules:
        - Always apologize first when there is a problem
        - Be polite and helpful
        - Answer clearly and naturally
        - If user asks follow-up questions, continue the conversation
        - If user asks about refund → explain timeline (3-5 days)

        Conversation:
        {history}

        Customer: {user_input}
        """

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",  # ✅ เสถียรกว่า 2.5
                contents=prompt
            )
            reply = response.text or "Sorry, I couldn't generate a response."

        except Exception as e:
            print("AI ERROR:", e)
            return "⚠️ Sorry, system error. Please try again."

        # ✅ save memory
        chat_history.append(f"Customer: {user_input}")
        chat_history.append(f"Agent: {reply}")

        # ✅ limit memory จริง
        chat_history = chat_history[-6:]

        return reply


