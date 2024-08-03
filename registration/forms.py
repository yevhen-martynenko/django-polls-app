from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label='username', 
        max_length=100, 
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )

    email = forms.EmailField(
        label='email', 
        max_length=35, 
        min_length=5, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )

    password = forms.CharField(
        label='password', 
        max_length=64, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )

    confirm_password = forms.CharField(
        label='confirm password', 
        max_length=64, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
