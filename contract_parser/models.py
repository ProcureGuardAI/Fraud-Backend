from django.db import models

class Contract(models.Model):
    contract_number = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    award_date = models.DateField(null=True, blank=True)
    tender_title = models.CharField(max_length=255)
    eval_completion_date = models.DateField(null=True, blank=True)
    notification_of_award_date = models.DateField(null=True, blank=True)
    sign_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    agpo_certificate_number = models.CharField(max_length=255)
    awarded_agpo_group_id = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    terminated = models.BooleanField(default=False)
    financial_year = models.IntegerField(null=True, blank=True)
    quarter = models.IntegerField(null=True, blank=True)
    tender_ref = models.CharField(max_length=255)
    pe_name = models.CharField(max_length=255)
    supplier_name = models.CharField(max_length=255)
    no_of_boi = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contract_number