import uuid
from django.db import models
from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
# New Movie Model - Details for adding to list a new movie into the database
# Includes: Title, Age Rating, Description, Runtime

class movieListing(models.Model):
    movieRating_CHOICES = (
        ('Universal', 'U'),
        ('Parental Guidance', 'PG'),
        ('12 Guidance ', '12A'),
        ('12 And Over ', '12'),
        ('15 and Over', '15'),
        ('18 and over', '18'),
        ('18 Special', '18R'),
    )

    movieTitle = models.CharField(max_length=300)
    movieDescription = models.CharField(max_length=300)
    movieRunTimeMinutes = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)], default=1)
    movieRating = models.CharField(max_length=300,choices=movieRating_CHOICES,default='Universal')

    def __str__(self):
        return (self.movieTitle)

# New Screen Model - Details for adding a new screening room into the database
# Includes: Screen Name, Screen Number, Seat Capacity

class addNewScreen(models.Model):
    movieScreenName = models.CharField(max_length=300)
    movieScreen = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)], default=1, unique=True)
    movieScreenSeatCapacity = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)], default=1)

    def __str__(self):
        return self.movieScreenName + ' | Screen No: ' + str(self.movieScreen)

# Movie Time Slot Model - Details for a showing of a film into the database, uses data from Screen and MovieListing
# Includes: Movie, Screening room, Date and Time
class movieTimeSlots(models.Model):
    movieDesired = models.ForeignKey(movieListing, default=1, on_delete=models.SET_DEFAULT)
    movieScreen = models.ForeignKey(addNewScreen, default=1, on_delete=models.SET_DEFAULT)
    movieTime = models.DateTimeField()
    movieDate = models.DateField()

    def __str__(self):
        date = (self.movieTime)
        return str(self.movieDesired) + ' is playing at: ' + str(date) + ' in screen: ' + str(self.movieScreen)

class pickMovie(models.Model):
    movieTitle = models.ForeignKey(movieListing, default=1, on_delete=models.SET_DEFAULT)
    movieTime = models.ForeignKey(movieTimeSlots, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return 'Your chosen movie is ' + str(self.movieTitle) + ' at ' + str(self.movieTime)

class pickUser(models.Model):
    roles_CHOICES = (
        ('Admin', 'Admin'),
        ('movie Manager', 'Movie Manager'),
        ('Club Rep', 'Club Rep'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    role = models.CharField(max_length=300,choices=roles_CHOICES,default='Admin')

class ClubRep(models.Model):
    accountNumber = models.UUIDField(max_length=255, default = uuid.uuid4)
    accountPassword = models.UUIDField(max_length=255, default = uuid.uuid4)

    firstname = models.CharField(max_length=300)
    surname = models.CharField(max_length=300)
    dateOfBirth = models.DateField(max_length=8)

    street = models.CharField(max_length=300)
    streetnumber = models.CharField(max_length=300)
    cr_city = models.CharField(max_length=300)
    cr_postcode = models.CharField(max_length=300)
    
    cr_email = models.EmailField()
    cr_landline = models.IntegerField()
    cr_mobile = models.IntegerField()
