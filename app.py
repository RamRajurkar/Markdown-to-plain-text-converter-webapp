from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, request, redirect, url_for, session, flash
import markdown2
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import google.generativeai as genai
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages


utc_time = datetime.utcnow()

# Define IST timezone offset (UTC + 5:30)
ist_offset = timedelta(hours=5, minutes=30)
ist_timezone = timezone(ist_offset)

# Convert UTC to IST
ist_time = utc_time.replace(tzinfo=timezone.utc).astimezone(ist_timezone)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "password")

# MongoDB Atlas connection
client = MongoClient(os.environ["MONGO_URI"])
db = client['MD_Converter']  # Replace with your database name
feedback_collection = db['Feedback']  # Collection to store feedbacks

# Create the model for text summarization
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

    feedback_submitted = request.args.get('feedback_submitted')

    if request.method == 'POST':
            markdown_text = request.form.get('markdown_text', '').strip()
            
            # Check if the input is empty and show an error message
            if not markdown_text:
                flash('Please enter some Markdown text before submitting!', 'danger')
            else:
                if 'convert_button' in request.form:
                    plain_text = markdown_to_text(markdown_text)
                    action = 'convert'
                elif 'summarize_button' in request.form:
                    try:
                        response = chat_session.send_message(markdown_text)
                        summary_text = markdown_to_text(response.text)
                        action = 'summarize'
                    except Exception as e:
                        flash('There was an error processing the summarization. Please try again.', 'danger')

        
    return render_template('index.html', plain_text=plain_text, summary_text=summary_text, action=action, markdown_text=markdown_text, feedback_submitted=feedback_submitted)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    feedback_text = request.form.get('feedback')

    if name and email and feedback_text:
        feedback = {
            "name": name,
            "email": email,
            "feedback": feedback_text,
            "submitted_at": ist_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        print(feedback)
        feedback_collection.insert_one(feedback)  # Save feedback to MongoDB

        flash('Thank you for your feedback!', 'success')
    else:
        flash('Please fill in all fields.', 'danger')

    return redirect(url_for('index', feedback_submitted=True))

################# FEEDBACK PAGE ##########################3 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        

        # Check if username and password match admin credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('feedbacks'))
        else:
            flash('Invalid credentials. Please try again.')
    
    return render_template('login.html')


@app.route('/feedbacks')
def feedbacks():
    # Check if admin is logged in
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    all_feedbacks = list(feedback_collection.find())  # Fetch feedbacks
    return render_template('feedbacks.html', feedbacks=all_feedbacks)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)  # Remove admin login state
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
