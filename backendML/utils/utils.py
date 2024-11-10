import PyPDF2
import re
import logging
import datetime

# Configure logger
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    logger.debug("Extracted text: %s", text)
    return text

def process_contract_data(text):
    contract_data = {}

    contract_number_match = re.search(r'Contract Number: (\d+)', text)
    contract_data['contract_number'] = contract_number_match.group(1) if contract_number_match else ''

    contract_amount_match = re.search(r'Contract Amount: (\d+\.?\d*)', text)
    contract_data['amount'] = float(contract_amount_match.group(1)) if contract_amount_match else 0.0

    award_date_match = re.search(r'Award Date: (\d{1,2}/\d{1,2}/\d{4})', text)
    contract_data['award_date'] = datetime.datetime.strptime(award_date_match.group(1), '%m/%d/%Y').date() if award_date_match else None

    tender_title_match = re.search(r'Tender Title: (.*)', text)
    contract_data['tender_title'] = tender_title_match.group(1) if tender_title_match else ''

    eval_completion_date_match = re.search(r'Evaluation Completion Date: (\d{1,2}/\d{1,2}/\d{4})', text)
    contract_data['eval_completion_date'] = datetime.datetime.strptime(eval_completion_date_match.group(1), '%m/%d/%Y').date() if eval_completion_date_match else None

    notification_of_award_date_match = re.search(r'Notification of Award Date: (\d{1,2}/\d{1,2}/\d{4})', text)
    contract_data['notification_of_award_date'] = datetime.datetime.strptime(notification_of_award_date_match.group(1), '%m/%d/%Y').date() if notification_of_award_date_match else None

    sign_date_match = re.search(r'Sign Date: (\d{1,2}/\d{1,2}/\d{4})', text)
    contract_data['sign_date'] = datetime.datetime.strptime(sign_date_match.group(1), '%m/%d/%Y').date() if sign_date_match else None

    start_date_match = re.search(r'Start Date: (\d{1,2}/\d{1,2}/\d{4})', text)
    contract_data['start_date'] = datetime.datetime.strptime(start_date_match.group(1), '%m/%d/%Y').date() if start_date_match else None

    end_date_match = re.search(r'End Date: (\d{1,2}/\d{1,2}/\d{4})', text)
    contract_data['end_date'] = datetime.datetime.strptime(end_date_match.group(1), '%m/%d/%Y').date() if end_date_match else None

    agpo_certificate_number_match = re.search(r'AGPO Certificate Number: (\d+)', text)
    contract_data['agpo_certificate_number'] = agpo_certificate_number_match.group(1) if agpo_certificate_number_match else ''

    awarded_agpo_group_id_match = re.search(r'Awarded AGPO Group ID: (\d+)', text)
    contract_data['awarded_agpo_group_id'] = awarded_agpo_group_id_match.group(1) if awarded_agpo_group_id_match else ''

    created_by_match = re.search(r'Created By: (.*)', text)
    contract_data['created_by'] = created_by_match.group(1) if created_by_match else ''

    terminated_match = re.search(r'Terminated: (Yes|No)', text)
    contract_data['terminated'] = terminated_match.group(1) == 'Yes' if terminated_match else False

    financial_year_match = re.search(r'Financial Year: (\d{4})', text)
    contract_data['financial_year'] = int(financial_year_match.group(1)) if financial_year_match else None

    quarter_match = re.search(r'Quarter: (\d)', text)
    contract_data['quarter'] = int(quarter_match.group(1)) if quarter_match else None

    tender_ref_match = re.search(r'Tender Ref: (.*)', text)
    contract_data['tender_ref'] = tender_ref_match.group(1) if tender_ref_match else ''

    pe_name_match = re.search(r'PE Name: (.*)', text)
    contract_data['pe_name'] = pe_name_match.group(1) if pe_name_match else ''

    supplier_name_match = re.search(r'Supplier Name: (.*)', text)
    contract_data['supplier_name'] = supplier_name_match.group(1) if supplier_name_match else ''

    no_of_boi_match = re.search(r'Number of BOI: (\d+)', text)
    contract_data['no_of_boi'] = int(no_of_boi_match.group(1)) if no_of_boi_match else None

    return contract_data