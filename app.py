from flask import Flask, render_template, request
import markdown2
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are an AI designed to create very concise summaries of given text. Your goal is to capture only the key points and essential information, avoiding any unnecessary details. The summary should be brief, specific, and no longer than a few sentences, while still preserving the main ideas and meaning of the original content."
)

chat_session = model.start_chat(history=[])

def markdown_to_text(markdown_string):
    html = markdown2.markdown(markdown_string)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

@app.route('/', methods=['GET', 'POST'])
def index():
    plain_text = ""
    summary_text = ""
    action = ""
    markdown_text = ""

    if request.method == 'POST':
        markdown_text = request.form.get('markdown_text', '')
        
        if 'convert_button' in request.form:
            plain_text = markdown_to_text(markdown_text)
            action = 'convert'
        elif 'summarize_button' in request.form:
            response = chat_session.send_message(markdown_text)
            summary_text = markdown_to_text(response.text)
            action = 'summarize'
    
    return render_template('index.html', plain_text=plain_text, summary_text=summary_text, action=action, markdown_text=markdown_text)

if __name__ == '__main__':
    app.run(debug=True)
