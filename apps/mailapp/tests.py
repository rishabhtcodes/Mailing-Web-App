from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from apps.users.models import CustomUser
from apps.mailapp.models import EmailHistory


class MailAppViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='sender@example.com', password='Password123!')
        self.other_user = CustomUser.objects.create_user(email='other@example.com', password='Password123!')
        self.send_url = reverse('mailapp:send_email')
        self.inbox_url = reverse('mailapp:inbox')

    def test_inbox_direct_access_without_login(self):
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)

    def test_inbox_renders_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mailapp/inbox.html')

    def test_send_email_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.send_url, {
            'recipient': 'recipient@example.com',
            'subject': 'Test Subject',
            'message': 'Hello World!',
        })
        self.assertEqual(response.status_code, 302)
        
        # Check email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertEqual(mail.outbox[0].to, ['recipient@example.com'])
        
        # Check EmailHistory created
        self.assertTrue(EmailHistory.objects.filter(user=self.user, recipient='recipient@example.com').exists())

    def test_send_email_missing_fields(self):
        self.client.force_login(self.user)
        response = self.client.post(self.send_url, {
            'recipient': 'recipient@example.com',
            'subject': '',
            'message': 'Hello World!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

    def test_email_history_isolation(self):
        EmailHistory.objects.create(
            user=self.user,
            sender_email='user@example.com',
            recipient='rec1@example.com',
            subject='Subject 1 Unique Title',
            message='Msg 1'
        )
        EmailHistory.objects.create(
            user=self.other_user,
            sender_email='other@example.com',
            recipient='rec2@example.com',
            subject='Subject 2 Secret Title',
            message='Msg 2'
        )

        self.client.force_login(self.user)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subject 1 Unique Title')
        self.assertNotContains(response, 'Subject 2 Secret Title')
