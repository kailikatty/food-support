import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

chat_history = []

def generate_ai_response(user_input, intent=None):
    history = "\n".join(chat_history)

prompt = f"""
You are a friendly and professional food delivery support agent.

Guidelines:
- Always start with empathy (e.g. "I'm really sorry...")
- Sound natural, like a real human agent
- Keep responses short (1-2 sentences)
- If it's about refund, explain clearly
- If user asks follow-up, continue the conversation naturally

Conversation:
{history}

Customer: {user_input}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    reply = response.text

    # save memory
    chat_history.append(f"Customer: {user_input}")
    chat_history.append(f"Agent: {reply}")

    return reply
