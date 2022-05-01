from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from MovieManaging.models import *

from django import forms
from django.contrib.auth.models import User, Group


class movieListingForm(forms.ModelForm):
    class Meta:
        model = movieListing
        fields = ("movieTitle","movieDescription","movieRunTimeMinutes","movieRating",) 

class addNewScreenForm(forms.ModelForm):
    class Meta:
        model = addNewScreen
        fields = ("movieScreenName", "movieScreen","movieScreenSeatCapacity",)

class movieTimetableForm(forms.ModelForm):
    class Meta:
        model = movieTimeSlots
        fields = ("movieDesired", "movieScreen", "movieTime",)

class movieSelectionForm(forms.Form):
        model = ModelChoiceField(queryset=movieTimeSlots.objects.all())

class pickUserForm(forms.ModelForm):
    class Meta:
        model = pickUser
        fields = ("user", "role",)

class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'

class pickTimeForm(forms.Form):
    date = forms.DateField(widget=MyDateInput())
