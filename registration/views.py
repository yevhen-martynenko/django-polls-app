from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone

from .forms import UserRegistrationForm
from .models import ActivationCode
from polls.utils import create_code

# TODO implementing additional security measures, such as CSRF protection, rate limiting on authentication attempts, and ensuring sensitive data is properly encrypted.

# TODO create my own encryption method instead of urlsafe_base64_encode, urlsafe_base64_decode


ACCOUNT_URL = 'registration:account'
SIGN_IN_URL = 'registration:sign_in'
SIGN_UP_URL = 'registration:sign_up'
RESET_PASSWORD_URL = 'registration:reset_password'
RESET_URL = 'registration:reset'


def sign_in(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     try:
    #         validate_email(username)
    #         is_email = True
    #     except ValidationError:
    #         is_email = False

    #     if is_email:
    #         user = authenticate(email=username, password=password)
    #     else:
    #         user = authenticate(username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         redirect_url = request.GET.get('next', 'index')
    #         return redirect(redirect_url)
    #     else:
    #         if is_email:
    #             messages.error(request, 'Email or Password is incorrect!')
    #         else:
    #             messages.error(request, 'Username or Password is incorrect!')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            validate_email(username)
            is_email = True
        except ValidationError:
            is_email = False

        user = None
        user_exists = False

        if is_email:
            try:
                user_exists = User.objects.filter(email=username).exists()
            except User.DoesNotExist:
                user_exists = False

            if user_exists:
                user = authenticate(email=username, password=password)
        else:
            try:
                user_exists = User.objects.filter(username=username).exists()
            except User.DoesNotExist:
                user_exists = False

            if user_exists:
                user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'index')
            return redirect(redirect_url)
        else:
            if not user_exists:
                if is_email:
                    messages.error(request, 'Email does not exist!')
                else:
                    messages.error(request, 'Username does not exist!')
            else:
                messages.error(request, 'Incorrect password!')

    page = {
        'title': 'Sign In',
    }

    return render(request, 'registration/sign_in.html', page)


def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            email = form.cleaned_data['email']

            try:
                validate_password(password)
            except Exception as e:
                for error in e:
                    messages.error(request, error)
                return redirect(SIGN_UP_URL)

            if password != confirm_password:
                messages.error(request, 'Password did not match!')
                return redirect(SIGN_UP_URL)

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect(SIGN_UP_URL)

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return redirect(SIGN_UP_URL)

            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.is_active = False
            user.save()

            try:
                host = request.get_host()
                code = create_code(32)
                activation_code = ActivationCode(user=user, code=code)
                activation_code.save()

                subject = f'Activate your account on {host}'
                template = render_to_string('email/activation_template.html', {
                    'user': user.username,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'code': urlsafe_base64_encode(force_bytes(code)),
                    'protocol': request.scheme,
                    'host': host,
                    'site_name': 'polls',
                })

                email_message = EmailMessage(
                    subject,
                    template,
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                if email_message.send():
                    messages.info(
                        request, f'Activate your account by email {email}.')
                else:
                    messages.error(
                        request, f'Unable to send email to {email}.')
            except Exception as e:
                messages.error(request, e)
                user.delete()
                return redirect(SIGN_UP_URL)
            else:
                user.save()
                return redirect(SIGN_IN_URL)
        else:
            messages.error(request, 'Form is not valid!')
    else:
        form = UserRegistrationForm()

    page = {
        'form': form,
        'title': 'Sign Up',
    }

    return render(request, 'registration/sign_up.html', page)


def activate(request, uidb64, code):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        decoded_code = force_str(urlsafe_base64_decode(code))
        user = get_object_or_404(User, pk=uid)
        activation_code = get_object_or_404(ActivationCode, user=user)
    except Exception:
        messages.error(request, 'Activation link is invalid!')
        return redirect('index')

    if activation_code.is_expired():
        user.delete()
        activation_code.delete()
        messages.error(request, 'Activation link is expired!')
        return redirect('index')

    if decoded_code == activation_code.code:
        user.is_active = True
        user.save()
        activation_code.delete()
        for _ in messages.get_messages(request):
            continue
        messages.success(
            request, f'Thanks for registering {user.username}.')
        return redirect(SIGN_IN_URL)
    else:
        try:
            user.delete()
            activation_code.delete()
            messages.error(request, 'Activation link is invalid!')
        except Exception:
            messages.error(request, 'Unable to activate account!')
    return redirect('index')


@login_required
def sign_out(request):
    logout(request)
    return redirect('index')


@login_required
def account(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')

        if password:
            new_password = request.POST.get('new_password')
            new_username = request.POST.get('new_username')
            new_email = request.POST.get('new_email')

            if user.check_password(password):
                if new_password:
                    if new_password == password:
                        messages.error(
                            request, 'New password must be different from the current one!')
                        return redirect(ACCOUNT_URL)
                    else:
                        try:
                            validate_password(new_password)
                        except Exception as e:
                            for error in e:
                                messages.error(request, error)
                            return redirect(ACCOUNT_URL)
                        else:
                            user.set_password(new_password)
                if new_username:
                    if User.objects.filter(username=new_username).exists():
                        messages.error(
                            request, f'Username "{new_username}" already exists!')
                        return redirect(ACCOUNT_URL)
                    elif new_username == user.username:
                        messages.error(
                            request, 'New username must be different from the current one!')
                        return redirect(ACCOUNT_URL)
                    else:
                        form = UserRegistrationForm({'username': new_username})
                        try:
                            for error in form.errors['username']:
                                messages.error(
                                    request, f'Username error "{error}"!')
                            return redirect(ACCOUNT_URL)
                        except KeyError:
                            user.username = new_username
                if new_email:
                    if User.objects.filter(email=new_email).exists():
                        messages.error(
                            request, f'Email "{new_email}" already registered!')
                        return redirect(ACCOUNT_URL)
                    elif new_email == user.email:
                        messages.error(
                            request, 'New email must be different from the current one!')
                        return redirect(ACCOUNT_URL)
                    else:
                        form = UserRegistrationForm({'email': new_email})
                        try:
                            for error in form.errors['email']:
                                messages.error(
                                    request, f'Email error "{error}"!')
                            return redirect(ACCOUNT_URL)
                        except KeyError:
                            user.email = new_email

                user.save()
                messages.success(
                    request, 'Account information successfully changed!')
            else:
                messages.error(request, 'Incorrect password')
                return redirect(ACCOUNT_URL)

            if new_password:
                if new_username:
                    user = authenticate(
                        username=new_username, password=new_password)
                else:
                    user = authenticate(
                        username=user.username, password=new_password)
            else:
                if new_username:
                    user = authenticate(
                        username=new_username, password=password)
                else:
                    user = authenticate(
                        username=user.username, password=password)

            login(request, user)

        return redirect(ACCOUNT_URL)

    extra_context = {
        'Host': request.headers.get('Host'),
        'Referer': request.headers.get('Referer'),
        'User agent': request.headers.get('User-Agent'),
        'Accept language': request.headers.get('Accept-Language'),

        'Server name': request.META.get('SERVER_NAME'),
        'Server port': request.META.get('SERVER_PORT'),
        'Server protocol': request.META.get('SERVER_PROTOCOL'),
        'Path info': request.META.get('PATH_INFO'),
        'Remote address': request.META.get('REMOTE_ADDR'),
    }

    page = {
        'title': 'Account',
        'extra_context': extra_context,
    }

    return render(request, 'registration/account.html', page)


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')

        if password:
            if user.check_password(password):
                user.delete()
                logout(request)
                messages.error(request, 'Your account has been removed')
                return redirect('index')
            else:
                messages.error(request, 'Incorrect password')

    return redirect('registration:account')


def reset_password(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')

        if username_or_email:
            try:
                user = get_object_or_404(User, username=username_or_email)
            except Exception:
                try:
                    user = get_object_or_404(User, email=username_or_email)
                except Exception:
                    messages.error(request, 'Username or email not found')
                    return redirect(RESET_PASSWORD_URL)

            email = user.email
            host = request.get_host()

            code = create_code(32)
            activation_code = ActivationCode.objects.filter(user=user).first()
            if activation_code:
                activation_code.code = code
                activation_code.date = timezone.now()
                activation_code.save()
            else:
                activation_code = ActivationCode(user=user, code=code)
                activation_code.save()

            subject = f'Password reset link for {user.username}'
            template = render_to_string('email/reset_template.html', {
                'user': user.username,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'code': urlsafe_base64_encode(force_bytes(code)),
                'protocol': request.scheme,
                'host': host,
                'site_name': 'polls',
            })

            email_message = EmailMessage(
                subject,
                template,
                settings.EMAIL_HOST_USER,
                [email],
            )

            if email_message.send():
                messages.info(
                    request, f'Password reset link sent to {user.email}')
                return redirect(SIGN_IN_URL)
            else:
                messages.error(
                    request, f'Unable to send email to {email}.')
        else:
            messages.error(request, 'Please enter username or email')

        return redirect(RESET_PASSWORD_URL)

    page = {
        'title': 'Password reset',
    }

    return render(request, 'registration/reset_password.html', page)


def reset(request, uidb64, code):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            decoded_code = force_str(urlsafe_base64_decode(code))
            user = get_object_or_404(User, pk=uid)
            activation_code = get_object_or_404(ActivationCode, user=user)
        except Exception:
            messages.error(request, 'Activation link is invalid!')
            return redirect('index')

        if activation_code.is_expired():
            activation_code.delete()
            messages.error(request, 'Activation link is expired!')
            return redirect('index')

        if decoded_code == activation_code.code:
            if new_password != confirm_new_password:
                messages.error(request, 'Password did not match!')
                return redirect(RESET_URL, uidb64, code)
            elif user.check_password(new_password):
                messages.error(
                    request, 'New password must be different from the current one!')
                return redirect(RESET_URL, uidb64, code)
            else:
                try:
                    validate_password(new_password)
                except Exception as e:
                    for error in e:
                        messages.error(request, error)
                    return redirect(RESET_URL, uidb64, code)
                else:
                    user.set_password(new_password)
                    user.save()
            activation_code.delete()
        else:
            activation_code.delete()
            messages.error(request, 'Activation link is invalid!')
        return redirect(SIGN_IN_URL)

    page = {
        'title': 'Password reset confirm',
    }

    return render(request, 'registration/reset.html', page)
