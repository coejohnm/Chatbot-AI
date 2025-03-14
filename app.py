#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify, Response, render_template
import openai
import os
import time

app = Flask(__name__)

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Store conversation history
conversation_history = [
    {"role": "system", "content": "You are a professional mental health advisor. Provide advice in fluent Chinese to help users relieve anxiety."}
]

@app.route('/')
def index():
    """Serve the HTML UI."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle user input, call OpenAI API, and return AI response with streaming."""
    user_input = request.json.get("message")
    conversation_history.append({"role": "user", "content": user_input})

    # Limit conversation history to 10 messages
    if len(conversation_history) > 10:
        conversation_history.pop(1)

    def generate():
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=conversation_history,
                stream=True  # Enable streaming response
            )
            for chunk in response:
                if hasattr(chunk.choices[0].delta, "content"):  # Ensure content exists
                    yield chunk.choices[0].delta.content  # Send streamed text
                    time.sleep(0.05)  # Small delay for smooth typing effect
        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(generate(), content_type='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


# In[ ]:




