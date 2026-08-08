from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import EmailHistory
from apps.users.models import get_active_user


def _seed_demo_emails_if_empty(user):
    """Seed modern sample emails if user inbox is empty to populate the UI like the demo mockup."""
    if EmailHistory.objects.filter(user=user).exists():
        return

    sample_mails = [
        {
            'sender_email': 'Jhone@gmail.com',
            'recipient': user.email,
            'subject': 'Happy Birthday!!!',
            'message': (
                f"Hi, {user.username or 'Gilang Ananta'}\n\n"
                "Today you received a birthday gift from our team. We hope this small gift makes your day "
                "more special and full of smiles. Thank you for being a part of our journey together. "
                "Happy birthday! Wishing you success, health, and happiness always.\n\n"
                "Thank you for being a part of our journey together.\n\n"
                "Regards,\nJhone"
            ),
            'folder': 'inbox',
            'is_starred': True,
        },
        {
            'sender_email': 'scottie.wallen@company.com',
            'recipient': user.email,
            'subject': 'Scottie Wallen',
            'message': 'Each plan comes with different storage and bandwidth options. Please review the updated documentation.',
            'folder': 'inbox',
            'is_starred': False,
        },
        {
            'sender_email': 'king.user@tech.org',
            'recipient': user.email,
            'subject': 'King User',
            'message': 'Welcome to the platform! Check out your analytics and active integrations in your user dashboard.',
            'folder': 'inbox',
            'is_starred': True,
        },
        {
            'sender_email': 'martin.madsen@design.io',
            'recipient': user.email,
            'subject': 'Martin Rhiel Madsen',
            'message': 'Each plan comes with different storage specs. Attached are the updated wireframes for review.',
            'folder': 'inbox',
            'is_starred': False,
        },
        {
            'sender_email': 'davis.kenter@dev.com',
            'recipient': user.email,
            'subject': 'Davis Kenter',
            'message': 'The deployment pipeline has been updated with custom SMTP configurations.',
            'folder': 'inbox',
            'is_starred': False,
        },
        {
            'sender_email': 'rayna.ekstrom@domain.co',
            'recipient': user.email,
            'subject': 'Rayna Ekstrom Bothman',
            'message': 'Confirming our scheduled call for tomorrow at 10 AM EST.',
            'folder': 'inbox',
            'is_starred': True,
        },
    ]

    for data in sample_mails:
        EmailHistory.objects.create(user=user, **data)


def landing_view(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'landing.html', {
        'user': user,
        'active_tab': 'landing'
    })


def inbox_view(request):
    user = get_active_user(request)
    _seed_demo_emails_if_empty(user)

    search_query = request.GET.get('q', '').strip()
    emails = EmailHistory.objects.filter(user=user)

    if search_query:
        emails = emails.filter(
            subject__icontains=search_query
        ) | emails.filter(
            recipient__icontains=search_query
        ) | emails.filter(
            sender_email__icontains=search_query
        ) | emails.filter(
            message__icontains=search_query
        )

    emails = emails.order_by('-sent_at')

    # Selected Mail Detail
    selected_mail_id = request.GET.get('mail_id')
    selected_mail = None
    if selected_mail_id:
        selected_mail = emails.filter(id=selected_mail_id).first()
    if not selected_mail and emails.exists():
        selected_mail = emails.first()

    return render(request, 'mailapp/inbox.html', {
        'user': user,
        'emails': emails,
        'selected_mail': selected_mail,
        'search_query': search_query,
        'active_tab': 'inbox',
        'email_count': emails.count(),
    })


import json
from django.views.decorators.csrf import csrf_exempt
from .models import EmailHistory, EmailAttachment


def ai_assist_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    prompt = data.get('prompt', '')
    action = data.get('action', 'generate')
    provider = data.get('provider', '')
    tone = data.get('tone', '')

    user = get_active_user(request)
    provider = provider or user.llm_provider
    tone = tone or user.ai_tone_preference

    api_key = ''
    if provider == 'gemini':
        api_key = user.gemini_api_key
    elif provider == 'openai':
        api_key = user.openai_api_key
    elif provider == 'claude':
        api_key = user.anthropic_api_key
    elif provider == 'groq':
        api_key = user.groq_api_key

    from .ai_service import generate_or_refine_email
    result_text = generate_or_refine_email(
        prompt=prompt,
        action=action,
        provider=provider,
        api_key=api_key,
        tone=tone
    )

    return JsonResponse({
        'result': result_text,
        'provider': provider,
        'tone': tone
    })


def send_email_view(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient', '').strip()
        cc = request.POST.get('cc', '').strip()
        bcc = request.POST.get('bcc', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        uploaded_files = request.FILES.getlist('attachments')

        if not all([recipient, subject, message]):
            messages.error(request, 'Recipient, Subject, and Message are required.')
            return redirect('mailapp:inbox')

        user = get_active_user(request)
        from_email = user.get_from_email()

        try:
            connection = user.get_smtp_connection()
            
            cc_list = [c.strip() for c in cc.split(',') if c.strip()]
            bcc_list = [b.strip() for b in bcc.split(',') if b.strip()]

            email_obj = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=[recipient],
                cc=cc_list if cc_list else None,
                bcc=bcc_list if bcc_list else None,
                connection=connection,
            )

            # Attach uploaded files to outgoing email
            for f in uploaded_files:
                email_obj.attach(f.name, f.read(), f.content_type)
                f.seek(0)

            email_obj.send(fail_silently=False)

            # Store in EmailHistory database
            sent_record = EmailHistory.objects.create(
                user=user,
                sender_email=user.smtp_username or user.email,
                recipient=recipient,
                cc=cc,
                bcc=bcc,
                subject=subject,
                message=message,
                folder='sent'
            )

            # Store attachments in EmailAttachment
            for f in uploaded_files:
                content_type = f.content_type or ''
                fname = f.name.lower()
                if 'image' in content_type or fname.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    ftype = 'image'
                elif 'pdf' in content_type or fname.endswith('.pdf'):
                    ftype = 'pdf'
                elif 'audio' in content_type or fname.endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                    ftype = 'audio'
                elif fname.endswith(('.doc', '.docx', '.txt', '.csv')):
                    ftype = 'document'
                else:
                    ftype = 'other'

                EmailAttachment.objects.create(
                    email=sent_record,
                    file=f,
                    filename=f.name,
                    file_type=ftype,
                    file_size=f.size
                )

            smtp_info = f" via {user.smtp_username}" if user.use_custom_smtp else " (Demo Fallback)"
            messages.success(request, f'Email successfully sent to {recipient}{smtp_info}!')
            return redirect(f'/mail/inbox/?mail_id={sent_record.id}')

        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
            return redirect('mailapp:inbox')

    return redirect('mailapp:inbox')


def toggle_star_view(request, mail_id):
    user = get_active_user(request)
    email = get_object_or_404(EmailHistory, id=mail_id, user=user)
    email.is_starred = not email.is_starred
    email.save()
    return redirect(request.META.get('HTTP_REFERER', 'mailapp:inbox'))


def delete_email_view(request, mail_id):
    user = get_active_user(request)
    email = get_object_or_404(EmailHistory, id=mail_id, user=user)
    email.delete()
    messages.success(request, 'Email deleted.')
    return redirect('mailapp:inbox')


def home_view(request):
    user = get_active_user(request)
    return render(request, 'mailapp/placeholder.html', {
        'user': user,
        'title': 'Home Overview',
        'active_tab': 'home'
    })


def campaigns_view(request):
    user = get_active_user(request)
    return render(request, 'mailapp/placeholder.html', {
        'user': user,
        'title': 'Email Campaigns',
        'active_tab': 'campaigns'
    })


def contacts_view(request):
    user = get_active_user(request)
    return render(request, 'mailapp/placeholder.html', {
        'user': user,
        'title': 'Contacts Directory',
        'active_tab': 'contacts'
    })


def analytics_view(request):
    user = get_active_user(request)
    return render(request, 'mailapp/placeholder.html', {
        'user': user,
        'title': 'Analytics Dashboard',
        'active_tab': 'analytics'
    })


def integrations_view(request):
    user = get_active_user(request)
    return render(request, 'mailapp/placeholder.html', {
        'user': user,
        'title': 'API & App Integrations',
        'active_tab': 'integrations'
    })
