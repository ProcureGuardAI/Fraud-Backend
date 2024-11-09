import PyPDF2

def extract_text_from_pdf(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page).extractText()
    pdf_file.close()
    return text
