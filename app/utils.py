import fitz
from pdf2image import convert_from_bytes
import pytesseract
from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def is_image_pdf(file):
    try:
        file.seek(0)
        convert_from_bytes(file.read(), first_page=1, last_page=1)
        return True
    except Exception as e:
        if "pdfinfo" in str(e).lower():
            return True
        raise e

def extract_text_with_ocr(file):
    file.seek(0)
    pdf_images = convert_from_bytes(file.read())
    text = "".join(pytesseract.image_to_string(image) for image in pdf_images)
    return text

def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype='pdf')
    text = "".join(page.get_text() for page in pdf_document)
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
    
    summary_html = response.choices[0].message.content.strip()
    summary = summary_html.replace("\n", "<br>").replace("\n\n", "<br><br>")
    
    return summary