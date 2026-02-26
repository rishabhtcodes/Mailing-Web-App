from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Override the default id field to be compatible with MongoDB
    id = models.CharField(max_length=24, primary_key=True, editable=False)
    
    class Meta:
        db_table = 'auth_user'
    
    def save(self, *args, **kwargs):
        if not self.id:
            from bson.objectid import ObjectId
            self.id = str(ObjectId())
        super().save(*args, **kwargs)
