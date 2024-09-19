import os
from flask import Blueprint, request, jsonify, render_template
from .utils import is_image_pdf, extract_text_with_ocr, extract_text_from_pdf, generate_summary

main = Blueprint('main', __name__)


@main.route('/')
def index():
    print("Current working directory:", os.getcwd())  # Debugging line
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if not file or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format. Only PDF files are accepted.'}), 400

    pdf_text = extract_text_with_ocr(file) if is_image_pdf(file) else extract_text_from_pdf(file)
    summary = generate_summary(pdf_text)
    
    return render_template('result.html', summary=summary)