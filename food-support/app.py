from flask import Flask, render_template
from routes.chat_routes import chat_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import os
import google.generativeai as genai  # ✅ ต้อง import แบบนี้

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

# register route
app.register_blueprint(chat_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()