# from accounts.models import Account
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin

from accounts.models import *

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups']

class clubAccountForm(forms.ModelForm):
    class Meta:
        model = studentClub
        fields = ['accountTitle', 'discountPercentage']

class clubRepUsernamePasswordForm(forms.ModelForm):
     class Meta:
         model = ClubRep
         fields = ['accountNumber', 'accountPassword']

class clubAccountNumberForm(forms.ModelForm):
    class Meta:
        model = studentClub
        fields = ['accountNumber']

class clubRepForm(forms.ModelForm):
     class Meta:
         model = ClubRep
         fields = ['firstname', 'surname', 'dateOfBirth', 'accountEmail']

class addClubAccount(forms.ModelForm):
    class Meta:
        model = studentClub
        fields = ['club', 'accountTitle', 'discountPercentage']

class addClub(forms.ModelForm):
     class Meta:
         model = clubDetails
         fields = ['clubName', 'street', 'streetNum', 'city', 'postcode', 'email', 'landline', 'mobile']

class addClubRep(forms.ModelForm):
     class Meta:
         model = ClubRep
         fields = ['firstname', 'surname', 'dateOfBirth', 'accountEmail']

#New FV
class discountListForm(forms.ModelForm):
    class Meta:
        model = discountList
        fields = ("club", "newDiscountPercentage")

class clubRepLoginForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = ("accountNumber", "accountPassword")