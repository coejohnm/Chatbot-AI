#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify
import openai
import os

# ✅ 確保這一行在 `@app.route` 之前
app = Flask(__name__)

# 使用環境變數來保護 API Key（在 Render 設定）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  
client = openai.OpenAI(api_key="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") 

conversation_history = [
    {"role": "system", "content": "你是一個專業的心理健康顧問，請用流暢的中文幫助使用者緩解焦慮。"}
]

# ✅ 確保 `app` 已定義後，才宣告 API 路由
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    conversation_history.append({"role": "user", "content": user_input})

    if len(conversation_history) > 10:
        conversation_history.pop(1)

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=conversation_history
        )

        ai_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_response})

        print(f"AI 回應: {ai_response}")  # ✅ 確認 AI 有回應
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"❌ OpenAI API 錯誤: {e}")
        return jsonify({"error": "OpenAI API 失敗"}), 500

# ✅ 確保 Flask 正確啟動
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


# In[ ]:




