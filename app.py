from flask import Flask, request, render_template_string
from google import genai

app = Flask(__name__)

# Initialize the Gemini AI Client
client = genai.Client()

# Clean and Professional English UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Chatbot</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f4f7f6; color: #333; }
        .chat-box { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0,0,0,0.08); }
        h2 { color: #007bff; margin-bottom: 20px; }
        .form-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex: 1; padding: 12px; border-radius: 6px; border: 1px solid #ccc; font-size: 16px; }
        button { padding: 12px 24px; border-radius: 6px; background: #007bff; color: white; border: none; font-size: 16px; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #0056b3; }
        .response { padding: 20px; background: #f8f9fa; border-left: 5px solid #007bff; border-radius: 4px; font-size: 16px; line-height: 1.5; }
        .response strong { color: #007bff; display: block; margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="chat-box">
        <h2>Harshika's AI Chatbot 🤖</h2>
        <form method="POST" class="form-group">
            <input type="text" name="user_input" placeholder="Type your message here..." required>
            <button type="submit">Send</button>
        </form>
        
        {% if response %}
        <div class="response">
            <strong>AI Response:</strong>
            <p>{{ response }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    if request.method == "POST":
        user_message = request.form.get("user_input")
        
        # Connect to Gemini API
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
            )
            ai_response = response.text
        except Exception as e:
            ai_response = f"API Error: {str(e)}"
            
    return render_template_string(HTML_TEMPLATE, response=ai_response)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)