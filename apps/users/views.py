from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import CustomUser


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'input-field'
        self.fields['password2'].widget.attrs['class'] = 'input-field'
        self.fields['email'].widget.attrs['class'] = 'input-field'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email'].split('@')[0]
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))


def _apply_form_styles(form):
    for field in form.fields.values():
        existing = field.widget.attrs.get('class', '')
        field.widget.attrs['class'] = f"{existing} input-field".strip()
    return form


def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = EmailUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {email}!')
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = EmailAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html', {'user': request.user})
