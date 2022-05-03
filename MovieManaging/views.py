import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from MovieManaging.forms import *
from MovieManaging.models import *
from django.http import HttpResponse
from django.utils.timezone import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.views.generic import UpdateView, DeleteView, ListView


from django.contrib.auth.models import Group

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
            message = form.cleaned_data['date']
            print(message)
           # request.session['date'] = message
            #message.save()
           # so = movieTimeSlots.objects.filter(movieDate=message)
           # return render(request, '../pickTime.html', {'so': so})
            return redirect("../pickTime")
    else:
        return render(request, "MovieWebsite/bookMovie.html", {"form": form})

def bookMovieShowing(request):
    form = movieSelectionForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
            return redirect("../home")
    else:
        return render(request, "MovieWebsite/pickTime.html", {"form": form})

@login_required
@user_passes_test(isCinemaOrAccountsManager)
def allMovies(request):
    movie_list = movieListing.objects.all()
    return render(request, 'MovieWebsite/movieList.html', {'movie_list':movie_list})

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
@user_passes_test(isCinemaOrAccountsManager)
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
@user_passes_test(isCinemaOrAccountsManager)
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