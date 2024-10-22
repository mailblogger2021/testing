from django.db import models

class CowinData(models.Model):
    pincode = models.CharField(max_length=6)
    fee_type = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_capacity = models.IntegerField()
    available_capacity_dose1 = models.IntegerField()
    available_capacity_dose2 = models.IntegerField()
    min_age_limit = models.IntegerField()
    vaccine = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.pincode} - {self.vaccine}"
