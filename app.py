from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
from docx import Document
from fpdf import FPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and file.filename.endswith('.docx'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        pdf_path = convert_to_pdf(filepath)
        return send_file(pdf_path, as_attachment=True)

def convert_to_pdf(docx_path):
    pdf = FPDF()
    pdf.add_page()
    document = Document(docx_path)
    for para in document.paragraphs:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, para.text)
    pdf_output_path = docx_path.replace('.docx', '.pdf')
    pdf.output(pdf_output_path)
    return pdf_output_path

if __name__ == '__main__':
    app.run(debug=True)