from flask import Flask, render_template, request
import markdown2
from bs4 import BeautifulSoup

app = Flask(__name__)

def markdown_to_text(markdown_string):
    # Convert Markdown to HTML
    html = markdown2.markdown(markdown_string)
    
    # Use BeautifulSoup to remove HTML tags and return plain text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

@app.route('/', methods=['GET', 'POST'])
def index():
    plain_text = ""
    if request.method == 'POST':
        markdown_text = request.form.get('markdown_text')
        if markdown_text:
            plain_text = markdown_to_text(markdown_text)
    
    return render_template('index.html', plain_text=plain_text)

if __name__ == '__main__':
    app.run(debug=True)
