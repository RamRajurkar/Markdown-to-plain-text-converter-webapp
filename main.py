import markdown2
from bs4 import BeautifulSoup

def markdown_to_text(markdown_string):
    # Convert Markdown to HTML
    html = markdown2.markdown(markdown_string)
    
    # Use BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

# Example usage
markdown_text = """
# Header
This is some **bold** text and some *italic* text.
- Item 1
- Item 2
"""

plain_text = markdown_to_text(markdown_text)
print(plain_text)
