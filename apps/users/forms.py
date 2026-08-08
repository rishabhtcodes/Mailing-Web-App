from django import forms
from .models import CustomUser


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'sender_name',
            'use_custom_smtp',
            'smtp_host',
            'smtp_port',
            'smtp_use_tls',
            'smtp_username',
            'smtp_password',
        )
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. John Doe'}),
            'smtp_host': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. smtp.gmail.com'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': '587'}),
            'smtp_use_tls': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 rounded focus:ring-blue-500 border-gray-300'}),
            'smtp_username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'your_email@gmail.com'}),
            'smtp_password': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '••••••••••••••••', 'render_value': True}),
            'use_custom_smtp': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 rounded focus:ring-blue-500 border-gray-300'}),
        }
