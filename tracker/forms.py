from django.forms import ModelForm
from .models import Challenge, Profile
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django import forms

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter verification code'}))

class PhoneVerification(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'is_verified']
    
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['challenge', 'challenge_date']
        
    def __init__(self, user, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(ChallengeForm, self).save(commit=False)
        instance.profile = self.user.profile
        if commit:
            instance.save()
        return instance
