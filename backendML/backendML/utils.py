# FILE: backendML/utils.py

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
import logging
import re

logger = logging.getLogger(__name__)

def generate_and_send_report(template_name, data, description, pdf_path, recipient_email, prediction_result):
    try:
        # Ensure data is a dictionary
        if isinstance(data, list):
            data = {'contracts': data}
        
        template = get_template(template_name)
        report_content = template.render(data)
        
        # Format the prediction result in a user-friendly table
        first_model_response = prediction_result['first_model_response']['data'][0][1]
        second_model_response = prediction_result['second_model_response']
        features_used_for_prediction = prediction_result['features_used_for_prediction']
        
        # Remove hashtags using regex
        first_model_response = re.sub(r'#', '', first_model_response)
        
        fraud_status = "Fraudulent" if second_model_response == 1 else "Not Fraudulent"
        fraud_color = "red" if second_model_response == 1 else "green"
        
        email_body_html = f"""
        <html>
        <body>
            <h2>Contract Report</h2>
            <p>{description}</p>
            <h3>Prediction Result</h3>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>First Model Response</th>
                    <td>{first_model_response}</td>
                </tr>
                <tr>
                    <th>Second Model Response</th>
                    <td style="color: {fraud_color};">{fraud_status}</td>
                </tr>
                <tr>
                    <th>Features Used for Prediction</th>
                    <td>{features_used_for_prediction}</td>
                </tr>
            </table>
            <h3>Report Content</h3>
            {report_content}
            <h3>Conclusion</h3>
            <p>Based on the analysis, the document is <span style="color: {fraud_color};">{fraud_status}</span>.</p>
        </body>
        </html>
        """
        
        email_body_plain = f"""
        Contract Report

        {description}

        Prediction Result
        First Model Response: {first_model_response}
        Second Model Response: {fraud_status}
        Features Used for Prediction: {features_used_for_prediction}

        Report Content
        {report_content}

        Conclusion
        Based on the analysis, the document is {fraud_status}.
        """
        
        email = EmailMultiAlternatives(
            "Contract Report",
            email_body_plain,
            settings.EMAIL_HOST_USER,
            [recipient_email],
        )
        email.attach_alternative(email_body_html, "text/html")

        email.send()
        logger.info("Report sent successfully.")
    except Exception as e:
        logger.error(f"Error sending report: {e}")