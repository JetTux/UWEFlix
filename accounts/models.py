from django.db import models
from MovieManaging.models import userTokens
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
import time
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

@receiver(user_signed_up)
def user_signed_up_signal_handler(request, user, **kwargs):
    group = Group.objects.get(name='Student')
    user.groups.add(group)
    user.save()
    time.sleep(0.5)
    userTokenObject = userTokens(tokenWallet='0', user_id=user.id)
    userTokenObject.save()
    print(userTokenObject)

@receiver(user_logged_in)
def user_logged_in_signal_handler(request, user, **kwargs):
    global clubRepLoginSuccessful 
    clubRepLoginSuccessful = False

class clubDetails(models.Model):
    clubName = models.CharField(max_length=300, unique=True)
    street = models.CharField(max_length=300)
    streetNum = models.IntegerField()
    city = models.CharField(max_length=300)
    postcode = models.CharField(max_length=300)
    email = models.EmailField()
    landline = models.IntegerField()
    mobile = models.IntegerField()

    def __str__(self):
        return str(self.clubName)

class studentClub(models.Model):
    accountNumber = models.UUIDField(max_length=255, default = uuid.uuid4)
    club = models.ForeignKey(clubDetails, default=1, on_delete=models.SET_DEFAULT)
    accountTitle = models.CharField(max_length=300)
    discountPercentage = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return str(self.accountTitle)

class ClubRep(models.Model):
    accountNumber = models.UUIDField(max_length=255, default = uuid.uuid4)
    accountPassword = models.UUIDField(max_length=255, default = uuid.uuid4)
    club = models.ForeignKey(studentClub, default=1, on_delete=models.SET_DEFAULT)

    firstname = models.CharField(max_length=300)
    surname = models.CharField(max_length=300)
    dateOfBirth = models.DateField(max_length=8)
    accountEmail = models.EmailField()

    def __str__(self):
        return str(self.surname)

class discountList(models.Model):
    club = models.ForeignKey(studentClub, default=1, on_delete=models.SET_DEFAULT)
    newDiscountPercentage = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return "Club: " + str(self.club) + " New discount percentage: " + str(self.newDiscountPercentage)

class clubRepUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

