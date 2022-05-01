import email
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

# from accounts.forms import RegistrationForm, AccountAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth.models import User
from accounts.forms import *
from accounts.models import *
from MovieManaging.views import isAccountsManager

from django.core.mail import send_mail

def isCinemaManager(User):
    return User.groups.filter(name='Cinema Manager').exists()

def isCinemaOrAccountsManager(User):
    if User.groups.filter(name='Accounts Manager').exists():
        return User.groups.filter(name='Accounts Manager').exists()
    elif User.groups.filter(name='Cinema Manager').exists():
        return User.groups.filter(name='Cinema Manager').exists()

def isAccountsManager(User):
    return User.groups.filter(name='Accounts Manager').exists()

#def user_login(request):
#    if request.method == "POST":
#        username = request.POST['username']
#        password = request.POST['password']
#        user = authenticate(request, username=username, password=password)
#        if user is not None:
#            login(request, user)
#            return redirect('../../home')
#        else:
#            messages.success(request, ("Invalid login, please try again"))
#            return redirect('login')
#    else:
#        return render(request, 'authenticate/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('../../home')

#def session_timeout(request):
 #   request.session
 #   return

@login_required
@user_passes_test(isAccountsManager)
def allAccounts(request):
    User = get_user_model()
    users = User.objects.all()
    studentClubs = studentClub.objects.all()
    clubReps = ClubRep.objects.all()
    return render(request, 'account/accountList.html', {'users':users, 'studentClubs':studentClubs, 'clubReps':clubReps})

@login_required
@user_passes_test(isAccountsManager)
def viewClubRep(request, clubRep_id):
    clubRep = ClubRep.objects.get(pk= clubRep_id)
    send_mail(
            'New Login Details',
            'Here are your new login details. Account Number: '+ str(clubRep.accountNumber) +' Password: '+ str(clubRep.accountPassword),
            'Dont Reply <do_not_reply@domain.com>',
            [clubRep.accountEmail],
    )
    return render(request, 'account/viewClubRep.html', {'clubRep':clubRep})

@login_required
@user_passes_test(isCinemaOrAccountsManager)
def viewClub(request, studentClub_id):
    StudentClub = studentClub.objects.get(pk=studentClub_id)
    return render(request, 'account/viewClub.html', {'studentClub':StudentClub})

@login_required
@user_passes_test(isAccountsManager)
def updateUser(request, user_id):
    user = User.objects.get(pk=user_id)
    form = userForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect ('accountList')
    return render(request, 'account/updateUser.html', {'User':user, 'form': form})

@login_required
@user_passes_test(isAccountsManager)
def updateClubAccount(request, studentClub_id):
    StudentClub = studentClub.objects.get(pk=studentClub_id)
    form = clubAccountForm(request.POST or None, instance=StudentClub)

    if form.is_valid():
        form.save()
        return redirect ('accountList')
    return render(request, 'account/updateClub.html', {'studentClub':StudentClub, 'form': form})

@login_required
@user_passes_test(isAccountsManager)
def updateClubRep(request, clubRep_id):
    clubRep = ClubRep.objects.get(pk= clubRep_id)
    form = clubRepForm(request.POST or None, instance=clubRep)

    if form.is_valid():
        form.save()
        return redirect ('accountList')
    return render(request, 'account/updateClubRep.html', {'clubRep':clubRep, 'form': form})

@login_required
@user_passes_test(isAccountsManager)
def createClubAccount(request):
    form = addClubAccount(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../../home")
    else:
        return render(request, "account/addClubAccount.html", {"form": form})

@login_required
@user_passes_test(isCinemaOrAccountsManager)
def clubRegister(request):  
    form = addClub(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.save()

            return redirect('../../home')
    else:
        return render(request, 'account/registerClub.html', {'form': form})

@login_required
@user_passes_test(isCinemaOrAccountsManager)
def clubRepRegister(request):  
    form = addClubRep(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect('../../home')
    else:
        return render(request, 'account/registerClubRep.html', {'form': form})

#New FV
@login_required
@user_passes_test(isCinemaOrAccountsManager)
def discountRequests(request):
    requests = discountList.objects.all()
    return render(request, 'account/discountRequests.html', {'requests':requests})

def updateDiscount(request, discountList_club):
    Club = studentClub.objects.get(club__clubName=discountList_club)
    form = clubAccountForm(request.POST or None, instance=Club)
    form.fields["accountTitle"].disabled = True
    if form.is_valid():
        form.save()
        return redirect ('discountRequests')
    return render(request, 'account/updateDiscount.html', {'club':Club, 'form': form})

def deleteDiscount(request, discountList_id):
    discountRequest = discountList.objects.get(pk=discountList_id)
    discountRequest.delete()
    return redirect ('discountRequests')

#@login_required
#@user_passes_test(isClubRep)
def requestDiscount(request):
    form = discountListForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../../home")
    else:
        return render(request, "account/requestDiscount.html", {"form": form})

#def deleteMovies(request, movie_id):
#    movie = movieListing.objects.get(pk=movie_id)
#    movie.delete()
#    return redirect ('movie_List')

# def register_view(request, *args, **kwargs):
# 	user = request.user
# 	if user.is_authenticated: 
# 		return HttpResponse("You are already authenticated as " + str(user.email))

# 	context = {}
# 	if request.POST:
# 		form = RegistrationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			email = form.cleaned_data.get('email').lower()
# 			raw_password = form.cleaned_data.get('password1')
# 			account = authenticate(email=email, password=raw_password)
# 			login(request, account)
# 			destination = kwargs.get("next")
# 			if destination:
# 				return redirect(destination)
# 			return redirect('../home')
# 		else:
# 			context['registration_form'] = form

# 	else:
# 		form = RegistrationForm()
# 		context['registration_form'] = form
# 	return render(request, 'account/register.html', context)

# def logout_view(request):
# 	logout(request)
# 	return redirect("../home")


# def login_view(request, *args, **kwargs):
# 	context = {}

# 	user = request.user
# 	if user.is_authenticated: 
# 		return redirect("../home")

# 	destination = get_redirect_if_exists(request)
# 	print("destination: " + str(destination))

# 	if request.POST:
# 		form = AccountAuthenticationForm(request.POST)
# 		if form.is_valid():
# 			email = request.POST['email']
# 			password = request.POST['password']
# 			user = authenticate(email=email, password=password)

# 			if user:
# 				login(request, user)
# 				if destination:
# 					return redirect(destination)
# 				return redirect("../home")

# 	else:
# 		form = AccountAuthenticationForm()

# 	context['login_form'] = form

# 	return render(request, "account/login.html", context)


# def get_redirect_if_exists(request):
# 	redirect = None
# 	if request.GET:
# 		if request.GET.get("next"):
# 			redirect = str(request.GET.get("next"))
# 	return redirect