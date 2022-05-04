from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

@receiver(user_signed_up)
def user_signed_up_signal_handler(request, user, **kwargs):
    group = Group.objects.get(name='Student')
    user.groups.add(group)
    user.save()

@receiver(user_logged_in)
def user_logged_in_signal_handler(request, user, **kwargs):
    global clubRepLoginSuccessful 
    clubRepLoginSuccessful = False

class clubDetails(models.Model):
    clubName = models.CharField(max_length=300)
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

#New FV
class discountList(models.Model):
    club = models.ForeignKey(studentClub, default=1, on_delete=models.SET_DEFAULT)
    newDiscountPercentage = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return "Club: " + str(self.club) + " New discount percentage: " + str(self.newDiscountRate)

class clubRepUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)


# class MyAccountManager(BaseUserManager):
# 	def create_user(self, email, username, password=None):
# 		if not email:
# 			raise ValueError('Users must have an email address')
# 		if not username:
# 			raise ValueError('Users must have a username')

# 		user = self.model(
# 			email=self.normalize_email(email),
# 			username=username,
# 		)

# 		user.set_password(password)
# 		user.save(using=self._db)
# 		return user
	
# 	def create_accountsmanager(self, email, username, password=None):
# 		user = self.create_user(
# 			email=self.normalize_email(email),
# 			password=password,
# 			username=username,
# 		)
# 		user.is_accountsmanager = True
# 		user.save()
# 		return user

# 	def create_moviemanager(self, email, username, password=None):
# 		user = self.create_user(
# 			email=self.normalize_email(email),
# 			password=password,
# 			username=username,
# 		)
# 		user.is_moviemanager = True
# 		user.save()
# 		return user

# 	def create_clubrep(self, email, username, password=None):
# 		user = self.create_user(
# 			email=self.normalize_email(email),
# 			password=password,
# 			username=username,
# 		)
# 		user.is_clubrep = True
# 		user.save()
# 		return user

# 	def create_superuser(self, email, username, password):
# 		user = self.create_user(
# 			email=self.normalize_email(email),
# 			password=password,
# 			username=username,
# 		)
# 		user.is_admin = True
# 		user.is_staff = True
# 		user.is_superuser = True
# 		user.save(using=self._db)
# 		return user



# class Account(AbstractBaseUser):
# 	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
# 	username 				= models.CharField(max_length=30, unique=True)
# 	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
# 	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
# 	is_admin				= models.BooleanField(default=False)
# 	is_active				= models.BooleanField(default=True)
# 	is_staff				= models.BooleanField(default=False)
# 	is_superuser			= models.BooleanField(default=False)
# 	hide_email				= models.BooleanField(default=True)

# 	is_accountsmanager = models.BooleanField(default=False)
# 	is_moviemanager = models.BooleanField(default=False)
# 	is_clubrep = models.BooleanField(default=False)

# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['username']

# 	objects = MyAccountManager()

# 	def __str__(self):
# 		return self.username

# 	# For checking permissions. to keep it simple all admin have ALL permissons
# 	def has_perm(self, perm, obj=None):
# 		return self.is_admin

# 	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
# 	def has_module_perms(self, app_label):
# 		return True

# class user(AbstractUser):
# 	is_accountsmanager = models.BooleanField(default=False)
# 	is_moviemanager = models.BooleanField(default=False)
# 	is_clubrep = models.BooleanField(default=False)
