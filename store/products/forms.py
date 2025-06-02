from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from products.models import *
from django import forms


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'input-container', 'placeholder' : 'Введите логин', 'id':'login'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'input-container', 'placeholder' : 'Введите пароль', 'id':'password', 
        
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-container', 'placeholder': 'Введите имя', 'id': 'name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-container', 'placeholder': 'Введите фамилию', 'id': 'surname'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'input-container', 'placeholder': 'Введите почту', 'id': 'e-mail'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-container', 'placeholder': 'Введите логин', 'id': 'login'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-container', 'placeholder': 'Введите пароль', 'id': 'password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input-container', 'placeholder': 'Подтвердите пароль', 'id': 'confirm password'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

class UserProfileForm(UserChangeForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-container', 'id': 'name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-container', 'id': 'name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-container', 'id': 'login'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'input-container', 'id': 'e-mail'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class BookingForm(forms.Form):
    
    checkin = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date', 'class': 'date-input', 'placeholder': 'Дата въезда'
    }))
    checkout = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date', 'class': 'date-input', 'placeholder': 'Дата выезда'
    }))
    type_choices = [
        ('', 'type'), ('single', 'single'), ('superior', 'superior'), ('family', 'family'),
    ]
    room_type = forms.ChoiceField(choices=type_choices, widget=forms.Select(attrs={
        'class': 'custom-select', 'id': 'comboBox1'
    }))

    room_choices = [
        ('', 'rooms'), (1, 1), (2, 2),
    ]
    rooms = forms.ChoiceField(choices=room_choices, widget=forms.Select(attrs={
        'class': 'custom-select', 'id': 'comboBox2'
    }))

