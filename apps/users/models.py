from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        if not username:
            username = email.split('@')[0]
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username=username, password=password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.CharField(max_length=24, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    sender_name = models.CharField(max_length=150, blank=True, default='')
    
    # Custom User SMTP Settings
    use_custom_smtp = models.BooleanField(default=False)
    smtp_host = models.CharField(max_length=255, blank=True, default='smtp.gmail.com')
    smtp_port = models.IntegerField(default=587)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_username = models.CharField(max_length=255, blank=True, default='')
    smtp_password = models.CharField(max_length=255, blank=True, default='')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    
    class Meta:
        db_table = 'auth_user'
    
    def save(self, *args, **kwargs):
        if not self.id:
            from bson.objectid import ObjectId
            self.id = str(ObjectId())
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def get_smtp_connection(self):
        from django.core.mail.backends.smtp import EmailBackend
        from django.core.mail import get_connection
        from django.conf import settings

        if self.use_custom_smtp and self.smtp_host and self.smtp_username and self.smtp_password:
            return EmailBackend(
                host=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                use_tls=self.smtp_use_tls,
                fail_silently=False,
            )
        
        return get_connection(backend=settings.EMAIL_BACKEND, fail_silently=False)

    def get_from_email(self):
        sender = self.sender_name or self.username or self.email.split('@')[0]
        if self.use_custom_smtp and self.smtp_username:
            return f"{sender} <{self.smtp_username}>"
        return f"{sender} <{self.email}>"


def get_active_user(request=None):
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    
    demo_user, _ = CustomUser.objects.get_or_create(
        email='rinanose@gmail.com',
        defaults={
            'username': 'Rina Nose',
            'sender_name': 'Rina Nose',
            'use_custom_smtp': False,
        }
    )
    return demo_user



