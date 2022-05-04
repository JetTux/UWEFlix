import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.views import View
from MovieManaging.forms import *
from MovieManaging.models import *
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.views.generic import UpdateView, DeleteView, ListView
from django.db.models import Avg
from django.contrib.auth.models import Group
from django.db.models import Sum
import accounts.views 
dateMessage = 0

def isCinemaManager(User):
    return User.groups.filter(name='Cinema Manager').exists()

def isAccountsManager(User):
    return User.groups.filter(name='Accounts Manager').exists()

def home(request):
    return HttpResponse("Hello, Django!")

#def hello_there2(request, name):
def hello_there(request, name):
    return render(
        request,
        'MovieWebsite/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def homePage(request):
    return render(request, "MovieWebsite/home.html")

def geeks_view(request):
    # create a dictionary to pass
    # data to the template
    context ={
        "data":"Gfg is the best",
        "list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    # return response with template and context
    return render(request, "MovieWebsite/home.html", context)

#https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544
def listNewMovie(request):
    form = movieListingForm(request.POST or None)

    group_required = u"Student"

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../home")
    else:
        return render(request, "MovieWebsite/listMovie.html", {"form": form})

# Can be used by any visitor, begins booking process
# Involves: movieTitle, movieTime
# Need to work on displaying only times for selected movie
#@login_required
def pickShowingTime(request):
    form = pickTimeForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            global dateMessage
            dateMessage = form.cleaned_data['date']
            print(dateMessage)
            return redirect("movieShowings")
    else:
        print(form)
        return render(request, "MovieWebsite/bookMovie.html", {"form": form})

def addTokensToWallet(request):
    form = tokenForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect("../home")
    else:
        return render(request, "MovieWebsite/addTokens.html", {"form": form})

def showTokenWallet(request):
    token_value = userTokens.objects.filter(user=request.user.id)
    return render(request, 'MovieWebsite/viewTokens.html', {'token_value':token_value})


def updateTokenWallet(request, wallet_id):
    tokens = userTokens.objects.get(pk=wallet_id)
    print(userTokens.objects.filter(user=request.user.id).aggregate(Avg('tokenWallet')))
    #print(movieTimeSlots.objects.filter(id=1).aggregate(Avg('moviePrice')))
    #print(movieTimeSlots.objects.filter(id=1).aggregate('moviePrice')
    #userTokens.objects.annotate(total_difference=F(''))

    form = tokenForm(request.POST or None, instance=tokens)

    if form.is_valid():
        form.save()
        return redirect ('home')
    return render(request, 'MovieWebsite/updateWallet.html', {'tokens':tokens, 'form': form})

def displayMovieBookings(request):
    bookingList = pickMovie.objects.filter(user=request.user.id)
    return render(request, 'MovieWebsite/bookingListings.html', {'bookingList':bookingList})

@login_required
@user_passes_test(isCinemaManager)
def allMovies(request):
    movie_list = movieListing.objects.all()
    return render(request, 'MovieWebsite/movieList.html', {'movie_list':movie_list})

def allShowings(request):
    global dateMessage
    if dateMessage == 0:
        showing_list = movieTimeSlots.objects.all().order_by('movieDate')
    else:
        showing_list = movieTimeSlots.objects.filter(movieDate__range=[dateMessage, dateMessage]).order_by('movieDate')
        dateMessage = 0
    return render(request, 'MovieWebsite/movieShowings.html', {'showing_list':showing_list})

def allShowingsClubRep(request):
    global dateMessage
    if dateMessage == 0:
        showing_list = movieTimeSlots.objects.all().order_by('movieDate')
    else:
        showing_list = movieTimeSlots.objects.filter(movieDate__range=[dateMessage, dateMessage]).order_by('movieDate')
        dateMessage = 0
    return render(request, 'MovieWebsite/movieShowingsClubRep.html', {'showing_list':showing_list})


def bookShowing(request, screening_id):
    print(screening_id)
    screening = movieTimeSlots.objects.get(pk=screening_id)
    print(screening)
    form = movieSelectionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.movieTime_id = screening_id
            
            # Obtains the id value for the screen used.
            screeningChoice = movieTimeSlots.objects.get(id=screening_id)
            screeningID = screeningChoice.movieScreen_id
            print("Screen ID: " + str(screeningID))

            # Obtains the seat capacity at the movie screening.
            movieSeats = addNewScreen.objects.filter(id=screeningID)
            movieSeatsTotal = movieSeats.aggregate(Sum('movieScreenSeatCapacity'))
            movieSeatsTotalConverted = movieSeatsTotal['movieScreenSeatCapacity__sum']

            # Obtains the total tickets purchased for the movie screening.
            movieInstance = pickMovie.objects.filter(movieTime_id=screening_id)
            totalTicketsPurchased = movieInstance.aggregate(Sum('movieTicketQuanity'))
            totalTicketsPurchasedConverted = totalTicketsPurchased['movieTicketQuanity__sum']

            # Calculates the remaining seats for the movie showing.
            remainingSeats = movieSeatsTotalConverted - totalTicketsPurchasedConverted
            print("Remaining Seats: " + str(remainingSeats))

            # Takes the ticket quantity from the form.
            ticketQuantity = (form.data['movieTicketQuanity'])
            print(accounts.views.clubRepLoginSuccessful)
            if accounts.views.clubRepLoginSuccessful == True:
                if int(ticketQuantity) < 10:
                    messages.error(request, 'Sorry, Club reps have to purchase a minimum of 10 tickets')
                    return redirect ('../movieShowingsClubRep')

            # Obtains the ticket price for the selected showing.
            modelInstance = movieTimeSlots.objects.get(id=screening_id)
            ticketPrice = modelInstance.moviePrice

            # Calculates the total token cost of the purchase.
            ticketCost = (int(ticketPrice) * int(ticketQuantity))

            if accounts.views.clubRepLoginSuccessful == True:
                print(ticketCost)
                print((int(accounts.views.discount)/100))
                discountAmount = ticketCost * (int(accounts.views.discount)/100)
                ticketCost = ticketCost - discountAmount 
                print(ticketCost)

            # Obtains the user's wallet.
            userWalletModel = userTokens.objects.get(user_id=request.user)
            userWallet = userWalletModel.tokenWallet
            print("Wallet before: " + str(userWallet))

            # Calculates the remaining tokens in the wallet.
            newUserWallet = (int(userWallet) - int(ticketCost))
            
            if remainingSeats > 0:
                if newUserWallet > 0:
                    userTokens.objects.filter(user=request.user).update(tokenWallet=newUserWallet)
                    message.save()    
                else:
                    print("Not Enough Tokens.")
            else:
                print("Not enough seats.")

            
            print("Wallet before: " + str(newUserWallet))
            return redirect ('movieShowings')
    else:
        return render(request, 'MovieWebsite/bookMovieShowing.html', {'screening':screening, 'form': form})

def bookMovieShowing(request):
    return render(request)


def updateMovies(request, movie_id):
    movie = movieListing.objects.get(pk=movie_id)
    form = movieListingForm(request.POST or None, instance=movie)

    if form.is_valid():
        form.save()
        return redirect ('movie_List')
    return render(request, 'MovieWebsite/updateMovie.html', {'movie':movie, 'form': form})

def deleteMovies(request, movie_id):
    movie = movieListing.objects.get(pk=movie_id)
    movie.delete()
    return redirect ('movie_List')

# Admin form allowing the creation of movie showing from the movieTimeTableForm
# Invloves: movieDesired, movieScreen, movieTime, movieDate

@login_required
@user_passes_test(isCinemaManager)
def createMovieShowing(request):
    form = movieTimetableForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../home")
    else:
        return render(request, "MovieWebsite/showingMovie.html", {"form": form})

# Admin form allowing the creation of a new screen.
# Involves: movieScreenName, movieScreen
# Need to work on not allowing 2 of the same number of screens

#@permission_required('auth.admin')
@login_required
@user_passes_test(isCinemaManager)
def screenAdder(request):
    form = addNewScreenForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../home")
    else:
        return render(request, "MovieWebsite/newScreen.html", {"form": form})

#@permission_required('auth.admin')
def chooseUserRole(request):
    form = pickUserForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../home")
    else:
        return render(request, "MovieWebsite/chooseRole.html", {"form": form})