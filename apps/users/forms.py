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
            'llm_provider',
            'gemini_api_key',
            'openai_api_key',
            'anthropic_api_key',
            'groq_api_key',
            'ai_tone_preference',
        )
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. John Doe'}),
            'smtp_host': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g. smtp.gmail.com'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': '587'}),
            'smtp_use_tls': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-neutral-900 rounded border-gray-300'}),
            'smtp_username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'your_email@gmail.com'}),
            'smtp_password': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '••••••••••••••••', 'render_value': True}),
            'use_custom_smtp': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-neutral-900 rounded border-gray-300'}),
            'llm_provider': forms.Select(attrs={'class': 'input-field'}),
            'gemini_api_key': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'AIzaSy...', 'render_value': True}),
            'openai_api_key': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'sk-proj-...', 'render_value': True}),
            'anthropic_api_key': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'sk-ant-...', 'render_value': True}),
            'groq_api_key': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'gsk_...', 'render_value': True}),
            'ai_tone_preference': forms.Select(choices=[
                ('professional', 'Professional'),
                ('persuasive', 'Persuasive'),
                ('short', 'Concise'),
                ('casual', 'Casual / Friendly'),
            ], attrs={'class': 'input-field'}),
        }

