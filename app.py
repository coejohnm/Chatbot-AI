#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify, render_template
import openai
import os

# Initialize Flask app and set template folder
app = Flask(__name__, template_folder="templates")

# Load API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Store conversation history
conversation_history = [
    {"role": "system", "content": "You are a professional mental health advisor. Please provide fluent Chinese responses to help users relieve anxiety."}
]

@app.route('/')
def index():
    """Serve the HTML UI."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle user input, call OpenAI API, and return AI response."""
    user_input = request.json.get("message")
    conversation_history.append({"role": "user", "content": user_input})

    # Limit conversation history to 10 messages
    if len(conversation_history) > 10:
        conversation_history.pop(1)

    try:
        # Call OpenAI API to generate response
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=conversation_history
        )

        ai_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_response})

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": f"OpenAI API Error: {e}"}), 500

if __name__ == '__main__':
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


# In[ ]:




