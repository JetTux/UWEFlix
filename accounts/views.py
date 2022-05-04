from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from MovieManaging.models import pickMovie
from accounts.forms import *
from accounts.models import *

from django.core.mail import send_mail

clubRepLoginSuccessful = False
discount = 0

def isCinemaManager(User):
    return User.groups.filter(name='Cinema Manager').exists()
def isStudent(User):
    return User.groups.filter(name='Student').exists()
def isCinemaOrAccountsManager(User):
    if User.groups.filter(name='Accounts Manager').exists():
        return User.groups.filter(name='Accounts Manager').exists()
    elif User.groups.filter(name='Cinema Manager').exists():
        return User.groups.filter(name='Cinema Manager').exists()

def isAccountsManager(User):
    return User.groups.filter(name='Accounts Manager').exists()

def clubRepLogin(request):
    global clubRepLoginSuccessful
    global discount
    if request.method == "POST":
            accountNum = request.POST['username']
            password = request.POST['password']
            if ClubRep.objects.filter(accountNumber=accountNum, accountPassword=password):
                clubRepLoginSuccessful = True

                clubRep = ClubRep.objects.get(accountNumber=accountNum)
                discount = clubRep.club.discountPercentage
                print(clubRepLoginSuccessful)
                return redirect('../../movieShowingsClubRep')
            else:
                clubRepLoginSuccessful = False
                return redirect('../loginClubRep')
    else:
        return render(request, 'account/loginClubRep.html')

def user_logout(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('../../home')

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
def allAccountStatements(request):
    accountStatements = pickMovie.objects.all()
    today = datetime.date.today()

    accountStatements = list(accountStatements.filter(created=today))
    return render(request, 'account/accountStatementList.html', {'accountStatements':accountStatements})

@login_required
@user_passes_test(isAccountsManager)
def statementsYear(request):
    accountStatements = pickMovie.objects.all()
    today = datetime.date.today()
    accountStatements = list(accountStatements.filter(created__year=today.year))
    return render(request, 'account/statementYear.html', {'accountStatements':accountStatements})

@login_required
@user_passes_test(isAccountsManager)
def statementsMonth(request):
    accountStatements = pickMovie.objects.all()
    today = datetime.date.today()
    accountStatements = list(accountStatements.filter(created__month=today.month, created__year=today.year))
    return render(request, 'account/statementMonth.html', {'accountStatements':accountStatements})

@login_required
@user_passes_test(isAccountsManager)
def notifyClubRep(request, clubRep_id):
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
            messages.info(request, 'Club Accounts Details Invalid.')
            return redirect('createClubAccount')
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
            messages.info(request, 'Club Details Invalid.')
            return redirect('registerClub')
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
            messages.info(request, 'Club Rep Details Invalid.')
            return redirect('registerClubRep')
    else:
        return render(request, 'account/registerClubRep.html', {'form': form})

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

def requestDiscount(request):
    form = discountListForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../../home")
        else:
            messages.info(request, 'Discount Invalid.')
            return redirect('requestDiscount')
    else:
        return render(request, "account/requestDiscount.html", {"form": form})
