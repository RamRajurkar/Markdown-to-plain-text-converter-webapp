# Markdown to Plain Text Converter

A simple web application that converts Markdown text into plain text and provides an option to summarize the content. This app uses Flask for the backend, Google Gemini API for summarization, and a user-friendly interface styled with HTML and Bootstrap.

## Features

- **Markdown to Plain Text Conversion:** Converts input Markdown into plain text.
- **Summarization:** Summarizes the provided text into a concise version.
- **Copy Functionality:** Copy the converted or summarized text with a single click.

## Technologies Used

- **Flask:** Python web framework used for the backend.
- **Google Gemini API:** For AI-powered summarization of the input text.
- **HTML/CSS/Bootstrap:** For the frontend design and styling.
- **JavaScript:** For interactive features like copying the result to the clipboard.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repo-name
    ```

3. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows: env\Scripts\activate
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up your environment variables:

    - Create a `.env` file in the root of your project.
    - Add the Google Gemini API key:
    
    ```plaintext
    GEMINI_API_KEY=your-google-gemini-api-key
    ```

6. Run the Flask app:

    ```bash
    flask run
    ```

7. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

1. **Convert Markdown:** Enter your Markdown text in the input box and click on the "Convert to Plain Text" button to get the plain text version.
2. **Summarize Text:** Click on the "Summarize" button to get a concise summary of the input text.
3. **Copy Text:** After conversion or summarization, click the "Copy" button to copy the result to your clipboard.


## Dependencies

- Flask
- markdown2
- BeautifulSoup4
- google-generativeai
- python-dotenv

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Gemini API](https://developers.google.com/gemini)
- [Bootstrap](https://getbootstrap.com/)
