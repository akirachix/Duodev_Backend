from django.db import models
from users.models import User
# Create your models here.
class Trader(User):
    number_of_posts = models.IntegerField()

    def __str__(self):
        return f"Trader {self.user_id} - {self.username}"