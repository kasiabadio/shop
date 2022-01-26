from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, required=True, help_text='Wymagane pole.')
    username = forms.CharField(max_length=50, required=True, help_text='Wymagane pole.')
    imie = forms.CharField(max_length=50, required=True, help_text='Wymagane pole.')
    nazwisko = forms.CharField(max_length=50, required=True, help_text='Wymagane pole.')
    is_producent = forms.BooleanField(required=False)
    is_klient = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ('email','username', 'imie', 'nazwisko', 'is_producent', 'is_klient' )
        
        
class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=60, required=True, help_text='Wymagane pole.')
    username = forms.CharField(max_length=50, required=True, help_text='Wymagane pole.')
    
    class Meta:
        model = User
        fields = ('email','username')