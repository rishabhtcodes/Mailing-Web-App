from django.db import models
from django.contrib.auth.models import User


class EmailHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    recipient = models.EmailField(max_length=254)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name_plural = 'Email Histories'

    def __str__(self):
        return f"{self.subject} to {self.recipient}"
