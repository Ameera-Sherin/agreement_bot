from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import fitz 
from pdf2image import convert_from_bytes
from openai import OpenAI
from dotenv import load_dotenv
import os
import pytesseract
from PIL import Image

app = Flask(__name__)
CORS(app)

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if not file or not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format. Only PDF files are accepted.'}), 400

    if is_image_pdf(file):
        pdf_text = extract_text_with_ocr(file)
    else:
        pdf_text = extract_text_from_pdf(file)
        
    summary = generate_summary(pdf_text)
    
    return render_template('result.html', summary=summary)

def is_image_pdf(file):
    try:
        file.seek(0)
        images = convert_from_bytes(file.read(), first_page=1, last_page=1)
        return True
    except Exception as e:
        if "pdfinfo" in str(e).lower():
            return True
        raise e

def extract_text_with_ocr(file):
    file.seek(0)
    pdf_images = convert_from_bytes(file.read())
    text = ""
    for image in pdf_images:
        text += pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype='pdf')
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def generate_summary(text):
    prompt = f"""
    Objective:
    Generate a concise and clear summary of a contract document. The summary should be well-structured and organized into labeled sections for easy understanding.

    Input:
    Contract Text DataFrame (df):
    This DataFrame contains the full text of a contract. The text may include various sections and legal jargon.
    
    Instructions:
    Identify and Extract Key Information:

    - Parties Involved: Identify the names of the parties involved in the contract.
    - Contract Type: Determine the type of the contract (e.g., NDA, Service Agreement).
    - Key Dates: Extract key dates from the contract (e.g., start date, termination date).
    - Financial Terms: Extract financial terms (e.g., payment schedule, pricing).
    - Important Clauses: Identify and extract key clauses (e.g., confidentiality, intellectual property).
    
    Format the Summary:

    Follow the provided format to draft the summary. Ensure that each section is clearly labeled and information is accurately extracted from the contract.
    
    Summary Format:
    <strong>This is a [[contract_type]] between [[parties]].</strong> The [[contract_type]] has an effective date of [[effective_date]] and is governed by the laws of [[governing_law]].
    
    Below is a summary of key terms of the contract.
    
    <strong>Purpose:</strong> [[purpose]]
    <strong>Confidentiality:</strong> [[confidentiality]]
    <strong>Term Date:</strong> [[term_date]]
    <strong>Termination Conditions:</strong> [[termination_conditions]]
    <strong>Representation:</strong> [[representation]]
    <strong>Guarantees and Warranties:</strong> [[guarantees_and_warranties]]
    <strong>Ownership:</strong> [[ownership]]
    
    In addition, below are details that you may find useful:
    <strong>Definitions:</strong> [[definitions]]
    <strong>Use and Care:</strong> [[use_and_care]]
    <strong>Disclosure Obligations:</strong> [[disclosure_obligations]]
    <strong>Non-Solicitation:</strong> [[non_solicitation]]
    <strong>Securities Compliance:</strong> [[securities_compliance]]
    <strong>Amendment Summary:</strong> [[amendment_summary]]
    <strong>Governing Law:</strong> [[governing_law_summary]]
    <strong>Notices and Execution:</strong> [[notices_and_execution]]
    
    Text:
    {text}
    """

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )

    summary = response.choices[0].message.content.strip()
    
    summary_html = summary.replace("\n", "<br>").replace("\n\n", "<br><br>")
    
    return summary_html

@app.route('/summary')
def summary_test():
    summary = """
    <strong>This is a Non-Disclosure Agreement between NA and 3M Company and Cogent, Inc..</strong> The Non-Disclosure Agreement has an effective date of 31/07/2008 and is governed by the laws of State of Minnesota.
    
    Below is a summary of key terms of the contract.
    
    <strong>Purpose:</strong> To protect and preserve the confidential and/or proprietary nature of certain information and materials of the Company that may be disclosed in connection with a potential transaction.
    <strong>Data protection and confidentiality:</strong> Receiving Party shall keep all Proprietary Information confidential and shall not disclose it without written consent from the Disclosing Party, except as required by law.
    <strong>Term date:</strong> 30/07/2012
    <strong>Termination Conditions:</strong> The obligations of this Agreement shall terminate on the second anniversary of the Effective Date, with certain sections surviving termination.
    <strong>Representation:</strong> Neither party makes any express or implied representation or warranty as to the completeness of the Proprietary Information.
    <strong>Guarantees and Warranties:</strong> Each party disclaims all warranties regarding the completeness of the Proprietary Information, including implied warranties of merchantability and fitness for a particular purpose.
    <strong>Ownership:</strong> All Proprietary Information remains the sole property of the Disclosing Party, while Derived Information is the sole property of the Receiving Party.
    
    In addition, below are details that you may find useful:
    <strong>Definitions:</strong>
    'Proprietary Information' encompasses all disclosed information related to the Proposed Transaction.
    <strong>Representatives:</strong> includes directors, officers, employees, and advisors of both parties.
    <strong>Use and Care:</strong>
    The Receiving Party may use Proprietary Information solely for evaluating the Proposed Transaction and must inform its Representatives of confidentiality obligations.
    Protection of Proprietary Information must be at least as diligent as the Receiving Party's own confidential information, but no less than reasonable care.
    <strong>Disclosure Obligations:</strong>
    In case of compelled disclosure by law, the Receiving Party must notify the Disclosing Party and attempt to limit the disclosure.
    <strong>Non-Solicitation:</strong>
    The Interested Party cannot solicit key personnel of the Company for three years from the Effective Date.
    <strong>Securities Compliance:</strong>
    Both parties recognize the legal restrictions on trading based on material non-public information.
    <strong>Amendment Summary:</strong>
    The non-solicitation period is extended to three years, and confidentiality obligations are extended to four years.
    <strong>Governing Law:</strong>
    The Agreement is governed by Minnesota law, disputes will be settled in California courts, and both parties waive their right to a jury trial.
    <strong>Notices and Execution:</strong>
    Communications must be in writing, and the Agreement can be executed in counterparts.
    """
    return render_template('result.html', summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
