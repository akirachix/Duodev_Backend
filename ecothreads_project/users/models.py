from django.db import models

# Define choices for the role field
# The choices are tuples containing the value to be stored in the database
# and the human-readable name for that value
ROLES = [
    ('admin', 'Admin'),
    ('seller', 'Seller'),
    ('recycler', 'Recycler'),
    ('public', 'Public User'),
]

class User(models.Model):
    # The primary key for the user model, an auto-incrementing integer
    user_id = models.AutoField(primary_key=True)
    # The username for the user, a unique string up to 150 characters
    username = models.CharField(max_length=150, unique=True)
    # The first name of the user, a string up to 30 characters
    first_name = models.CharField(max_length=30)
    # The last name of the user, a string up to 30 characters
    last_name = models.CharField(max_length=30)
    # The email address of the user, a unique string
    email = models.EmailField(unique=True)
    # The password for the user, a string up to 128 characters
    # Note: passwords should never be stored as plain text in a real application
    # This is just for demonstration purposes
    password = models.CharField(max_length=128)  
    # The phone number of the user, a string up to 15 characters
    # This field is optional
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # The date the user registered, automatically set to the current date
    registration_date = models.DateField(auto_now_add=True)
    # The role of the user, one of the choices defined in ROLES
    role = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        # Return the username as the string representation of the user
        return self.username

