from django.db import models
from traders.models import Trader

class TextileBale(models.Model):
    bale_id = models.AutoField(primary_key=True)
    trader = models.ForeignKey('traders.Trader', on_delete=models.CASCADE)  # FK to Trader
    waste_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    weight = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Bale {self.bale_id} - {self.waste_type} at {self.location}"


