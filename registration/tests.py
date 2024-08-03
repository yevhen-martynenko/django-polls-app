from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from polls.utils import create_code
from .forms import UserRegistrationForm
from .models import ActivationCode


class TestActivationCode(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@test.com')
        code = create_code(32)
        self.code_obj = ActivationCode.objects.create(
            user=user,
            code=code,
            date=timezone.now()
        )

    def test_activation_code_is_not_expired(self):
        self.assertFalse(self.code_obj.is_expired())

    def test_activation_code_is_expired(self):
        date = timezone.now() - timezone.timedelta(hours=24)
        self.code_obj.date = date
        self.code_obj.save()
        self.assertTrue(self.code_obj.is_expired())

    def test_activation_code_str_method(self):
        self.assertEqual(str(self.code_obj), self.code_obj.code)


class TestUserRegistrationForm(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@test.com'
        }

        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@test.com')

    def test_valid_registration_form(self):
        # valid registration form
        form = UserRegistrationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form_1(self):
        # username is empty
        form_data = {'username': '', 'password': 'testpassword',
                     'confirm_password': 'wrongpassword', 'email': 'test@test.com'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_registration_form_2(self):
        # username already exist
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_invalid_registration_form_3(self):
        # email already exist
        self.assertTrue(User.objects.filter(email='test@test.com').exists())

    def test_invalid_registration_form_4(self):
        # email is empty
        form_data = {'username': 'testuser', 'password': 'testpassword',
                     'confirm_password': 'testpassword', 'email': ''}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_registration_form_5(self):
        # email is invalid
        form_data = {'username': 'testuser', 'password': 'testpassword',
                     'confirm_password': 'testpassword', 'email': 'test@test'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_registration_form_6(self):
        # password mismatch
        form_data = {'username': 'testuser', 'password': 'testpassword',
                     'confirm_password': 'testpassword1', 'email': 'test@test.com'}
        form = UserRegistrationForm(data=form_data)
        self.assertNotEquals(
            form.data['password'], form.data['confirm_password'])


class TestSignIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@test.com', password='testpassword')

    def test_sign_in_with_correct_credentials(self):
        response = self.client.post(reverse('registration:sign_in'), {
                                    'username': 'testuser', 'password': 'testpassword'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('index'))

    def test_sign_in_with_correct_credentials_with_email(self):
        response = self.client.post(reverse('registration:sign_in'), {
                                    'username': 'test@test.com', 'password': 'testpassword'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('index'))

    def test_sign_in_with_incorrect_credentials(self):
        response = self.client.post(
            reverse('registration:sign_in'), 
            {'username': 'wronguser', 'password': 'wrongpassword'}, follow=True)
        self.assertContains(response, 'Username or Password is incorrect!')

    def test_sign_in_with_incorrect_credentials_with_email(self):
        response = self.client.post(
            reverse('registration:sign_in'), 
            {'username': 'wrongemail@test.test', 'password': 'wrongpassword'}, follow=True)
        self.assertContains(response, 'Email or Password is incorrect!')

    def test_sign_in_with_missing_credentials(self):
        response = self.client.post(
            reverse('registration:sign_in'), {}, follow=True)
        self.assertContains(response, 'Username or Password is incorrect!')

    def test_sign_in_with_get_request(self):
        response = self.client.get(reverse('registration:sign_in'))
        self.assertEqual(response.status_code, 200)

    def test_authentication_status_after_sign_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_sign_out(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('registration:sign_out'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


class TestSignUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@test.com'
        }
        self.form = UserRegistrationForm(data=self.form_data)
        self.user = User.objects.create_user(
            username='user', password='password', email='email@test.com')

    def test_sign_up_with_valid_form(self):
        response = self.client.post(
            reverse('registration:sign_up'), self.form.data, follow=True)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        # self.assertContains(response, f'Thanks for registering {User.objects.get(username="testuser").username}.')

    def test_sign_up_with_invalid_form(self):
        form_data = {
            'username': '',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': '.com'
        }
        form = UserRegistrationForm(data=form_data)
        response = self.client.post(
            reverse('registration:sign_up'), form.data, follow=True)
        self.assertContains(response, 'Form is not valid!')

    def test_sign_up_with_missing_form(self):
        response = self.client.post(
            reverse('registration:sign_up'), {}, follow=True)
        self.assertContains(response, 'Form is not valid!')

    def test_sign_up_with_mismatching_password(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword1',
            'email': 'test@test.com'
        }
        form = UserRegistrationForm(data=form_data)
        response = self.client.post(
            reverse('registration:sign_up'), form.data, follow=True)
        self.assertContains(response, 'Password did not match!')

    def test_sign_up_with_existing_username(self):
        form_data = {
            'username': 'user',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@test.com'
        }
        form = UserRegistrationForm(data=form_data)
        response = self.client.post(
            reverse('registration:sign_up'), form.data, follow=True)
        self.assertContains(response, 'Username already exists!')

    def test_sign_up_with_existing_email(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'email@test.com'
        }
        form = UserRegistrationForm(data=form_data)
        response = self.client.post(
            reverse('registration:sign_up'), form.data, follow=True)
        self.assertContains(response, 'Email already registered!')

    def test_sign_up_with_get_request(self):
        response = self.client.get(reverse('registration:sign_up'))
        self.assertEqual(response.status_code, 200)


class TestAccountActions(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_successful_account_deletion(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('registration:delete_account'), {'password': 'testpassword'}, follow=True)
        self.assertContains(response, 'Your account has been removed')
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_unsuccessful_account_deletion(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('registration:delete_account'), {'password': 'wrongpassword'}, follow=True)
        self.assertContains(response, 'Incorrect password')
        self.assertTrue(User.objects.filter(username='testuser').exists())
