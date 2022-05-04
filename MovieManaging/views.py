from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MovieManaging.forms import *
from MovieManaging.models import *
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import datetime
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg
from django.db.models import Sum
import accounts.views 
dateMessage = 0

def isCinemaManager(User):
    return User.groups.filter(name='Cinema Manager').exists()

def isCinemaOrAccountsManager(User):
    if User.groups.filter(name='Accounts Manager').exists():
        return User.groups.filter(name='Accounts Manager').exists()
    elif User.groups.filter(name='Cinema Manager').exists():
        return User.groups.filter(name='Cinema Manager').exists()

def isAccountsManager(User):
    return User.groups.filter(name='Accounts Manager').exists()

def home(request):
    return HttpResponse("Hello, Django!")


def homePage(request):
    movie_list = movieListing.objects.all()
    return render(request, "MovieWebsite/home.html", {'movie_list':movie_list})

def geeks_view(request):
    return redirect("../home")

def listNewMovie(request):
    form = movieListingForm(request.POST, request.FILES or None)

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

@login_required
def showTokenWallet(request):
    token_value = userTokens.objects.filter(user=request.user.id)
    return render(request, 'MovieWebsite/viewTokens.html', {'token_value':token_value})

@login_required
def updateTokenWallet(request, wallet_id):
    tokens = userTokens.objects.get(pk=wallet_id)
    print(userTokens.objects.filter(user=request.user.id).aggregate(Avg('tokenWallet')))
    form = tokenForm(request.POST or None, instance=tokens)

    if form.is_valid():
        form.save()
        return redirect ('showTokenWallet')
    return render(request, 'MovieWebsite/updateWallet.html', {'tokens':tokens, 'form': form})

@login_required
def displayMovieBookings(request):
    bookingList = pickMovie.objects.filter(user=request.user.id)
    return render(request, 'MovieWebsite/bookingListings.html', {'bookingList':bookingList})

@login_required
@user_passes_test(isCinemaOrAccountsManager)
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
    screening = movieTimeSlots.objects.get(pk=screening_id)
    form = movieSelectionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.user = request.user
                message.movieTime_id = screening_id
                
                # Obtains the id value for the screen used.
                screeningChoice = movieTimeSlots.objects.get(id=screening_id)
                screeningID = screeningChoice.movieScreen_id


                # Obtains the seat capacity at the movie screening.
                movieSeats = addNewScreen.objects.filter(id=screeningID)
                movieSeatsTotal = movieSeats.aggregate(Sum('movieScreenSeatCapacity'))
                movieSeatsTotalConverted = movieSeatsTotal['movieScreenSeatCapacity__sum']

                # Obtains the total tickets purchased for the movie screening.
                movieInstance = pickMovie.objects.filter(movieTime_id=screening_id)
                totalTicketsPurchased = movieInstance.aggregate(Sum('movieTicketQuanity'))
                totalTicketsPurchasedConverted = totalTicketsPurchased['movieTicketQuanity__sum']

                if totalTicketsPurchasedConverted == None:
                    totalTicketsPurchasedConverted = 0
                # Calculates the remaining seats for the movie showing.
                remainingSeats = movieSeatsTotalConverted - totalTicketsPurchasedConverted

                # Takes the ticket quantity from the form.
                ticketQuantity = (form.data['movieTicketQuanity'])
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
                    discountAmount = ticketCost * (int(accounts.views.discount)/100)
                    ticketCost = ticketCost - discountAmount 

                # Obtains the user's wallet.
                if userTokens.objects.get(user_id=request.user):
                    userWalletModel = userTokens.objects.get(user_id=request.user)
                    userWallet = userWalletModel.tokenWallet
                else:
                    messages.error(request, 'You have not created a wallet, please do so in the Initialise Tokens tab')
                    return redirect ('../movieShowings')
                print(remainingSeats)
                # Calculates the remaining tokens in the wallet.
                newUserWallet = (int(userWallet) - int(ticketCost))
                if remainingSeats > 0:
                    if newUserWallet > 0:
                        userTokens.objects.filter(user=request.user).update(tokenWallet=newUserWallet)
                        message.save()    
                        messages.info(request, 'Booking accepted, you can view your bookings in the View Bookings tab')
                        return redirect ('../movieShowings')
                    else:
                        messages.error(request, 'Sorry, You do not have enough tokens for this purchase')
                        return redirect ('../movieShowings')
                else:
                    messages.error(request, 'Sorry, there are not enough seats available')
                    return redirect ('../movieShowings')
            else:
                #user = models.ForeignKey(User, blank = True, null = True)
                #message.user = user
                message.movieTime_id = screening_id
                message.save()
                return redirect ('../movieShowings')
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

@login_required
@user_passes_test(isCinemaOrAccountsManager)
def allShowingsForUpdating(request):
    showing_list = movieTimeSlots.objects.all().order_by('movieDate')
    return render(request, 'MovieWebsite/allShowings.html', {'showing_list':showing_list})

def updateShowings(request, showing_id):
    showing = movieTimeSlots.objects.get(pk=showing_id)
    form = showingForm(request.POST or None, instance=showing)

    if form.is_valid():
        form.save()
        return redirect ('../../allShowings')
    return render(request, 'MovieWebsite/updateShowing.html', {'showing':showing, 'form': form})
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
            messages.info(request, 'Movie Screen Details Invalid')
            return redirect('newScreen')
    else:
        return render(request, "MovieWebsite/newScreen.html", {"form": form})

@login_required
@user_passes_test(isCinemaOrAccountsManager)
def cancellationRequests(request):
    requests = pickMovie.objects.filter(cancelRequested=True)
    return render(request, 'MovieWebsite/cancellationRequests.html', {'requests':requests})

def deleteBooking(request, pickMovie_id):
    booking = pickMovie.objects.get(pk=pickMovie_id)
    booking.delete()
    return redirect ('cancellationRequests')

def deleteRequest(request, pickMovie_id):
    cancelRequest = pickMovie.objects.get(pk=pickMovie_id)
    cancelRequest.cancelRequested = False
    cancelRequest.save()
    return redirect ('cancellationRequests')

def requestCancellation(request, booking_id):
    cancelRequest = pickMovie.objects.get(pk=booking_id)
    cancelRequest.cancelRequested = True
    cancelRequest.save()
    messages.info(request, 'Cancellation Request Sent.')
    return redirect ('../home')

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