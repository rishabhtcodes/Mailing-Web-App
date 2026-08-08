from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import CustomUser


class UsersModelTests(TestCase):
    def test_create_user_with_explicit_username(self):
        user = CustomUser.objects.create_user(email='test1@example.com', username='customname', password='Password123!')
        self.assertEqual(user.email, 'test1@example.com')
        self.assertEqual(user.username, 'customname')
        self.assertTrue(user.check_password('Password123!'))

    def test_create_user_auto_username(self):
        user = CustomUser.objects.create_user(email='test2@example.com', password='Password123!')
        self.assertEqual(user.email, 'test2@example.com')
        self.assertEqual(user.username, 'test2')

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(email='admin@example.com', password='AdminPassword123!')
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class UsersViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.settings_url = reverse('users:settings')
        self.inbox_url = reverse('mailapp:inbox')

    def test_register_page_renders(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user_success(self):
        response = self.client.post(self.register_url, {
            'email': 'newuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.inbox_url)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())

    def test_register_duplicate_email(self):
        CustomUser.objects.create_user(email='dup@example.com', password='Password123!')
        response = self.client.post(self.register_url, {
            'email': 'dup@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This email is already registered.')

    def test_login_page_renders(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        user = CustomUser.objects.create_user(email='user@example.com', password='Password123!')
        response = self.client.post(self.login_url, {
            'email': 'user@example.com',
            'password': 'Password123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.inbox_url)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': 'wrong@example.com',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password.')

    def test_logout(self):
        user = CustomUser.objects.create_user(email='user@example.com', password='Password123!')
        self.client.login(username='user@example.com', password='Password123!')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mailapp:landing'))

    def test_settings_direct_access_without_login(self):
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)

    def test_settings_authenticated(self):
        user = CustomUser.objects.create_user(email='user@example.com', password='Password123!')
        self.client.force_login(user)
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings.html')
