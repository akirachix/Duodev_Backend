from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.company_name
