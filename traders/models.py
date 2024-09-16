from django.db import models
from users.models import User

class Trader(User):
    number_of_posts = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = [
            ("post_products", "Can post products"),
        ]

    def __str__(self):
        return f"Trader {self.user_id} - {self.username}"
