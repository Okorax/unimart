from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from datetime import datetime

class UserRegisterForm(UserCreationForm):
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date(), 'class': 'form-control-custom'})
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'date_of_birth', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Add CSS classes to other fields
        self.fields['username'].widget.attrs.update({'class': 'form-control-custom'})
        self.fields['email'].widget.attrs.update({'class': 'form-control-custom'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control-custom'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control-custom'})
        
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control-custom'})
        self.fields['password'].widget.attrs.update({'class': 'form-control-custom'})