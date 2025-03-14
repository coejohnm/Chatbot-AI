#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify, Response, render_template
import openai
import os
import time

app = Flask(__name__)

# Use environment variable for API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

conversation_history = [
    {"role": "system", "content": "You are a professional mental health advisor. Provide advice in fluent Chinese to help users relieve anxiety."}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    conversation_history.append({"role": "user", "content": user_input})

    if len(conversation_history) > 10:
        conversation_history.pop(1)

    def generate():
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=conversation_history,
                stream=True  # Enable streaming
            )
            for chunk in response:
                if chunk.choices[0].delta.get("content"):
                    yield chunk.choices[0].delta["content"]  # Send chunked text
                    time.sleep(0.05)  # Add slight delay for smooth typing effect
        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(generate(), content_type='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


# In[ ]:




