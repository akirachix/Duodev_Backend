from django.db import models

# Define choices for the role field
ROLES = [
    ('admin', 'Admin'),
    ('seller', 'Seller'),
    ('recycler', 'Recycler'),
    ('public', 'Public User'),
]

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # No hashing, stored as plain text
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return self.username
