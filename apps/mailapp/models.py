from django.db import models
from django.conf import settings


class EmailHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emails')
    sender_email = models.EmailField(max_length=254, blank=True, default='')
    recipient = models.EmailField(max_length=254)
    cc = models.CharField(max_length=500, blank=True, default='')
    bcc = models.CharField(max_length=500, blank=True, default='')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_starred = models.BooleanField(default=False)
    folder = models.CharField(max_length=50, default='sent')

    class Meta:
        ordering = ['-sent_at']
        verbose_name_plural = 'Email Histories'

    def __str__(self):
        return f"{self.subject} to {self.recipient}"


class EmailAttachment(models.Model):
    email = models.ForeignKey(EmailHistory, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100) # image, pdf, audio, document, other
    file_size = models.BigIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} ({self.file_type})"


