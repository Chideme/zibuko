from django import forms
from django.core.exceptions  import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,label="Username")
    password = forms.CharField(max_length=100,label="Password",widget=forms.PasswordInput)
    
class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(max_length=100,label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100,label="Retype password",widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 >= password2:
            raise ValidationError("Passwords must be the same")