from django.db import models

class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    contract_name = models.CharField(max_length=255)
    contract_date = models.DateField()

    def __str__(self):
        return self.contract_name
    