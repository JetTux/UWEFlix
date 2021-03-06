import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User



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
    movieImage = models.ImageField(upload_to='images/')

    def __str__(self):
        return (self.movieTitle)

# New Screen Model - Details for adding a new screening room into the database
# Includes: Screen Name, Screen Number, Seat Capacity

class addNewScreen(models.Model):
    movieScreenName = models.CharField(max_length=300)
    movieScreen = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)], default=1, unique=True)
    movieScreenSeatCapacity = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(1)], default=1)

    def __str__(self):
        return self.movieScreenName + ' Number: ' + str(self.movieScreen)

# Movie Time Slot Model - Details for a showing of a film into the database, uses data from Screen and MovieListing
# Includes: Movie, Screening room, Date and Time
class movieTimeSlots(models.Model):
    movieDesired = models.ForeignKey(movieListing, default=1, on_delete=models.CASCADE)
    movieScreen = models.ForeignKey(addNewScreen, default=1, on_delete=models.CASCADE)
    movieTime = models.TimeField()
    movieDate = models.DateField()
    moviePrice = models.IntegerField(default=10)

    def __str__(self):

        return 'Movie Name: ' + str(self.movieDesired) + ' | On ' + str(self.movieDate) + ' at ' + str(self.movieTime) + ' | In Screen: ' + str(self.movieScreen) 
    
    def ticketingStr(self):
        return 'Movie Name: ' + str(self.movieDesired) + ' | On ' + str(self.movieDate) + ' at ' + str(self.movieTime) + ' | In Screen: ' + str(self.movieScreen)

    def ticketingPrice(self):
        return str(self.moviePrice)

class pickMovie(models.Model):
    movieTime = models.ForeignKey(movieTimeSlots, default=1, on_delete=models.CASCADE)
    movieTicketQuanity = models.IntegerField(default=1, validators=[MaxValueValidator(10000), MinValueValidator(0)])
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    cancelRequested = models.BooleanField(blank=True, null=True)
    customerEmail = models.EmailField()

    def __str__(self):
        return 'User: ' + str(self.user) + ' | ' + str(self.customerEmail) + ' | ' + str(self.movieTime.ticketingStr()) + ". Amount of tickets purchased: " + str(self.movieTicketQuanity) + " | Total Tokens Spent: " + str(self.movieTicketQuanity * int(self.movieTime.ticketingPrice()))

class userTokens(models.Model):
    tokenWallet = models.IntegerField(default=0, validators=[MaxValueValidator(10000), MinValueValidator(0)])
    user = models.OneToOneField(User, blank=True, unique=True, on_delete=models.CASCADE)


    def __str__(self):
        return "Hello " + str(self.user) + ", you have: " + str(self.tokenWallet) + " tokens in your wallet."