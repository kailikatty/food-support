import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

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

    response = model.generate_content(prompt)
    reply = response.text

    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Bot: {reply}")

    return reply