from django import forms
from.models import Contract
import re

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'

    def clean_contract_number(self):
        contract_number = self.cleaned_data['contract_number']
        pattern = r'^[a-zA-Z]{2}-\d{4}-\d{3}$'
        if not re.match(pattern, contract_number):
            raise forms.ValidationError("Invalid contract number")
        return contract_number

    def clean_contract_amount(self):
        contract_amount = self.cleaned_data['contract_amount']
        try:
            contract_amount = float(contract_amount)
            if contract_amount <= 0:
                raise forms.ValidationError("Invalid contract amount")
            return contract_amount
        except ValueError:
            raise forms.ValidationError("Invalid contract amount")

    def clean_award_date(self):
        award_date = self.cleaned_data['award_date']
        if award_date is None:
            raise forms.ValidationError("Invalid award date")
        return award_date

    def clean_eval_completion_date(self):
        eval_completion_date = self.cleaned_data['eval_completion_date']
        if eval_completion_date is None:
            raise forms.ValidationError("Invalid evaluation completion date")
        return eval_completion_date

    def clean_notification_of_award_date(self):
        notification_of_award_date = self.cleaned_data['notification_of_award_date']
        if notification_of_award_date is None:
            raise forms.ValidationError("Invalid notification of award date")
        return notification_of_award_date

    def clean_sign_date(self):
        sign_date = self.cleaned_data['sign_date']
        if sign_date is None:
            raise forms.ValidationError("Invalid sign date")
        return sign_date

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date is None:
            raise forms.ValidationError("Invalid start date")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date is None:
            raise forms.ValidationError("Invalid end date")
        return end_date

    def clean_agpo_certificate_number(self):
        agpo_certificate_number = self.cleaned_data['agpo_certificate_number']
        pattern = r'^[A-Za-z0-9]+$'
        if not re.match(pattern, agpo_certificate_number):
            raise forms.ValidationError("Invalid AGPO certificate number")
        return agpo_certificate_number

    def clean_awarded_agpo_group_id(self):
        awarded_agpo_group_id = self.cleaned_data['awarded_agpo_group_id']
        if not isinstance(awarded_agpo_group_id, int) or awarded_agpo_group_id < 1:
            raise forms.ValidationError("Invalid awarded AGPO group ID")
        return awarded_agpo_group_id

    def clean_created_by(self):
        created_by = self.cleaned_data['created_by']
        pattern = r'^[A-Za-z\s]+$'
        if not re.match(pattern, created_by):
            raise forms.ValidationError("Invalid created by")
        return created_by
    
    def clean_financial_year(self):
        financial_year = self.cleaned_data['financial_year']
        if not isinstance(financial_year, int) or financial_year < 1:
            raise forms.ValidationError("Invalid financial year")
        return financial_year

    def clean_quarter(self):
        quarter = self.cleaned_data['quarter']
        if not isinstance(quarter, int) or quarter < 1 or quarter > 4:
            raise forms.ValidationError("Invalid quarter")
        return quarter

    def clean_tender_ref(self):
        tender_ref = self.cleaned_data['tender_ref']
        if not isinstance(tender_ref, int) or tender_ref < 1:
            raise forms.ValidationError("Invalid tender reference")
        return tender_ref

    def clean_pe_name(self):
        pe_name = self.cleaned_data['pe_name']
        if not pe_name.isalpha():
            raise forms.ValidationError("Invalid PE name")
        return pe_name

    def clean_supplier_name(self):
        supplier_name = self.cleaned_data['supplier_name']
        if not supplier_name.isalpha():
            raise forms.ValidationError("Invalid supplier name")
        return supplier_name

    def clean_no_of_boi(self):
        no_of_boi = self.cleaned_data['no_of_boi']
        if not isinstance(no_of_boi, int) or no_of_boi < 1:
            raise forms.ValidationError("Invalid number of BOI")
        return no_of_boi

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError({"start_date": "Start date cannot be after end date"})
        return cleaned_data