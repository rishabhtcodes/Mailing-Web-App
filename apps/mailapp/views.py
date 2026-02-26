from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import EmailHistory


@login_required
def send_email_view(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if not all([recipient, subject, message]):
            messages.error(request, 'All fields are required.')
            return redirect('mailapp:send_email')
        
        try:
            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            # Store in database
            EmailHistory.objects.create(
                user=request.user,
                recipient=recipient,
                subject=subject,
                message=message
            )
            
            messages.success(request, f'Email sent successfully to {recipient}!')
            return redirect('mailapp:send_email')
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
            return redirect('mailapp:send_email')
    
    return render(request, 'mailapp/send_email.html')


@login_required
def email_history_view(request):
    emails = EmailHistory.objects.filter(user=request.user)
    return render(request, 'mailapp/email_history.html', {'emails': emails})
