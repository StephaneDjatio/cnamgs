from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}), label='Email')
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), label='Nom')
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), label='Prénom')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['role'].widget.attrs['class'] = 'form-control'

        self.fields['username'].label = 'Nom d\'utilisateur'
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmer mot de passe'
        self.fields['role'].label = 'Rôle'


