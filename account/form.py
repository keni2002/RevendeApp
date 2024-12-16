from django import forms
import re
from django.contrib.auth.models import User
from .models import Profile
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    
    #its good clean_<fieldname>() is a standard
    # def clean_password(self):
    #     cd = self.cleaned_data
    #     password = cd['password']
    #      # Check minimum length 
    #     if len(password) < 8:
    #         raise forms.ValidationError('The password must be at least 8 characters long.')
    #     # Check for at least one digit
    #     if not re.search(r'\d', password):
    #         raise forms.ValidationError('The password must contain at least one digit.')
    #     # Check for at least one uppercase letter 
    #     if not re.search(r'[A-Z]', password):
    #         raise forms.ValidationError('The password must contain at least one uppercase letter.')
    #     # Check for at least one lowercase letter 
    #     if not re.search(r'[a-z]', password): 
    #         raise forms.ValidationError('The password must contain at least one lowercase letter.')
    #     # Check for at least one special character 
    #     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #         raise forms.ValidationError('The password must contain at least one special character.') 
    #     return password
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    #prevent same email
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists() and data!='':
            raise forms.ValidationError('Email already in use')
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                        .filter(email=data)
        if qs.exists() and data!='':
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth','photo']