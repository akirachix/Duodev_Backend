from django.conf import settings
from django.db import models
from traders.models import Trader

class TextileBale(models.Model):
    """Model to represent textile bales."""
    
    bale_id = models.AutoField(primary_key=True)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, related_name='textile_bales')
    waste_type = models.CharField(max_length=255)  
    weight = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='textile_bales_posted', default=1)
    image = models.ImageField(upload_to='textile_bales/', blank=True, null=True)  
    
    class Meta:
        permissions = [
            ("post_textilebale_custom", "Can post textile bale"),
            ("view_textilebale_custom", "Can view textile bale"),
        ]

    def __str__(self):
        return f"Bale {self.bale_id} - {self.waste_type}"
