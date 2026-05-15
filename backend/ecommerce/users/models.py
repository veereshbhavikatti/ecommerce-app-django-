from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Set email as unique for authentication
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_seller = models.BooleanField(default=False)
    
    # Use email as the unique identifier for login instead of username
    USERNAME_FIELD = "email" 
    
    # Fields prompted when creating a superuser (excluding password and USERNAME_FIELD)
    REQUIRED_FIELDS = ["username"] 

    def __str__(self):
        return self.email 