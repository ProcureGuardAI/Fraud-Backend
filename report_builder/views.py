from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Contract
from Reportgen.settings import EMAIL_HOST_USER


class ReportBuilder:
    def __init__(self, template_name, data, description):
        self.template_name = template_name
        self.data = data
        self.description = description

    def generate_report(self, request):
        return render(request, self.template_name, self.data)

    def send_report(self, request, subject, to_email):
        report = self.generate_report(request).content.decode('utf-8')
        send_mail(subject, self.description, EMAIL_HOST_USER, [to_email], html_message=report)


def generate_report(request):
    contracts = Contract.objects.all()
    description = "This is a report of all contracts."
    report_builder = ReportBuilder('reports.html', {'contracts': contracts}, description)
    
    user_email = request.POST.get('user_email', 'clency2023@gmail.com')  # Get user email from request
    try:
        report_builder.send_report(request, "Contract Report", user_email)
        return HttpResponse("Report sent successfully!")
    except Exception as e:
        return HttpResponse(f"Failed to send report: {e}", status=500)