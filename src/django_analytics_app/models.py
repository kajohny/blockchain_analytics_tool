from django.db import models

class Address(models.Model):
    address_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    address_balance = models.IntegerField()

    def __str__(self):
        return f'{self.address_name} - {self.address_balance}'
