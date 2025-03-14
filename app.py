#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Store conversation history
conversation_history = [
    {"role": "system", "content": "You are a professional mental health support assistant. Your goal is to provide emotional support, stress management techniques, and positive coping strategies in a warm and compassionate tone. Adjust your language based on the user's input, responding in English."}
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    # Add user input to history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Ensure conversation history does not exceed 10 messages
    if len(conversation_history) > 10:
        conversation_history.pop(1)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=conversation_history,
            max_tokens=200  # Limit response length
        )
        
        ai_response = response.choices[0].message.content
        
        # Append AI response to history
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        return jsonify({"response": ai_response})
    
    except Exception as e:
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


# In[ ]:




