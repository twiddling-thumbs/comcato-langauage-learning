from django import forms
from .models import Language , Material


class LanguageAdminForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'  # Include all fields from the model

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['your_language','foreign_language', 'file', 'name','type']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    



