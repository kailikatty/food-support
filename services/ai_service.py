import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

chat_history = []

def generate_ai_response(user_input):
    history = "\n".join(chat_history)

    prompt = f"""
You are a professional food delivery support agent.
Be polite and helpful.

Conversation:
{history}

Customer: {user_input}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    reply = response.text

    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Bot: {reply}")

    return reply
