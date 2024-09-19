# Agreement Bot

## Description
Agreement Bot is a Python web application that allows users to upload PDF documents (both text and image-based) and receive concise summaries of their content. The application utilizes Optical Character Recognition (OCR) to extract text from image-based PDFs and employs OpenAI's GPT model to generate structured summaries.

## Features
- Upload PDF files (text/image) for summarization.
- Support for both text-based and image-based PDFs.
- Generate well-structured summaries with key information extracted from the documents.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Ameera-Sherin/agreement_bot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd pdf-summarizer
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment variables:
   - Create a `.env` file in the root directory and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage
1. Run the application:
   ```bash
   python run.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Upload a PDF file using the provided form and click "Submit" to receive a summary.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request. Ensure your code adheres to the project's coding standards.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```

3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message here"
   ```

4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```

5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to OpenAI for providing the GPT model.
- Thanks to the contributors and the open-source community for their support and inspiration.# agreement_bot
# agreement_bot
