#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify
import openai
import os

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Get OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is not set! Please configure it in your environment variables.")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Conversation history storage
conversation_history = [
    {"role": "system", "content": "You are a professional mental health counselor. Please provide helpful responses in fluent Chinese to help users relieve anxiety."}
]

# ✅ Default route for health check
@app.route("/")
def home():
    return "Chatbot API is running!"

# ✅ Chatbot API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # ✅ Add user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # ✅ Limit conversation history to 10 messages
    if len(conversation_history) > 10:
        conversation_history.pop(1)

    try:
        # ✅ Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=conversation_history
        )

        ai_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_response})

        print(f"✅ AI Response: {ai_response}")  # Log AI response
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return jsonify({"error": "OpenAI API request failed"}), 500

# ✅ Run Flask app in production mode using Gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)


# In[ ]:




