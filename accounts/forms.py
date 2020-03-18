from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput

#from .models import profile_extension
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        field = ('username','password')
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')



class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
    }))
    first_name=forms.CharField( max_length=100,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'First Name'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name',
        'readonly':'true'
    }))
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name','date_joined')


#class ProfileExtensionForm(forms.ModelForm):
#    profile_avatar=forms.ImageField(required=False)
#    user_id=forms.CharField
#    class Meta:
#        model=profile_extension
#        fields=('user_id','profile_avatar')


class PasswordChangeCustomForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          "कृपया सहcvbcी पासवर्ड दर्ज करें."}
    old_password = CharField(required=True, label='Συνθηματικό',
                             widget=PasswordInput(attrs={
                                 'class': 'form-control'}),
                             error_messages={
                                 'required': 'कृपया सही पासवर्ड दर्ज करें'})

    new_password1 = CharField(required=True, label='Συνθηματικό',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'कृपया सही पासवर्ड दर्ज करें'})
    new_password2 = CharField(required=True, label='Συνθηματικό (Επαναλάβατε)',
                              widget=PasswordInput(attrs={
                                  'class': 'form-control'}),
                              error_messages={
                                  'required': 'कृपया सही पासवर्ड दर्ज करें'})
