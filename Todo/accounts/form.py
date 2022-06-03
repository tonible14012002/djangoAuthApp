
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    password = forms.CharField(min_length=8, label='Password')
    password2 = forms.CharField(min_length=8, label='Password confirm')

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        if firstname:
            return firstname
        raise forms.ValidationError('First name is required')
    
    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        if lastname:
            return lastname
        raise forms.ValidationError('Last name is required')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email has been used')
        return email
    
    def clean_password2(self):
        confirm_password = self.cleaned_data['password2']
        if confirm_password == self.cleaned_data['password']:
            return confirm_password
        raise forms.ValidationError('Password confirm does not match')
