from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.CharField(max_length=24, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'auth_user'
    
    def save(self, *args, **kwargs):
        if not self.id:
            from bson.objectid import ObjectId
            self.id = str(ObjectId())
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
