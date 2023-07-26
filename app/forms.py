from django import forms 
from app.models import *
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password',]
        widgets={'password':forms.PasswordInput}
        help_texts={'username':'','first_name':'','last_name':''}


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_pic','address']

