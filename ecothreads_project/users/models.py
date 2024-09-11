# users/models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Define user roles
ROLES = [
    ('seller', 'Seller'),
    ('recycler', 'Recycler'),
    ('public', 'Public User'),
]

class UserManager(BaseUserManager):
    """Custom manager to handle user creation."""
    
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that uses 'username' as the unique identifier."""
    
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)  # Authentication field
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLES, default='public')
    
    # Control user status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Check if user has a specific permission."""
        if self.role == 'public' and perm in ['post_textilebale']:
            return False
        if self.role == 'seller' and perm in ['buy_textilebale']:
            return False
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        """Check if user has permissions to view the app 'app_label'."""
        return self.is_superuser

    class Meta:
        permissions = [
            ("post_textilebale_custom", "Can post textile bale"),
            ("buy_textilebale", "Can buy textile bale"),
            ("view_textilebale_custom", "Can view textile bale"),
        ]
