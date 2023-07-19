from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Add custom fields to the user model
    # Example: date_of_birth = models.DateField()

    # Optional: Customize the username field if needed
    # Example: username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    # Set the email field as the unique identifier for authentication
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users')
