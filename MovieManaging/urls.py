from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
#from accounts.forms import RegistrationForm
#from accounts.views import register_view, login_view, logout_view
from .views import *


#https://django-allauth.readthedocs.io/en/latest/installation.html
#pip install django-environ

urlpatterns = [
    path("showingMovie/", createMovieShowing, name="showingMovie"),
    path("bookMovie/", pickShowingTime, name="bookMovie"),
    path("newScreen/", screenAdder, name="newScreen"),
    path("listMovie/", listNewMovie, name="listMovie"),
    path("chooseRole/",chooseUserRole, name="chooseRole"),
    path('home/', homePage, name="homer"),
    path('', geeks_view, name="home"),
    path("pickTime/", bookMovieShowing, name="pickTime"),
    path("movies/", allMovies, name="movie_List"),
    path("updateMovie/<movie_id>", updateMovies, name='update_movie'),
    path("deleteMovie/<movie_id>", deleteMovies, name='delete_movie'),
    path("bookingListings/", displayMovieBookings, name='displayMovieBookings'),
    path("addTokens/", addTokensToWallet, name='addTokensToWallet'),
    path("viewTokens/", showTokenWallet, name='showTokenWallet'),
    path("updateWallet/<wallet_id>", updateTokenWallet, name='updateTokenWallet'),
    path("movieShowings/", allShowings, name='movieShowings'),
    path("bookMovieShowing/<screening_id>", bookShowing, name='bookMovieShowing'),
    path("movieShowingsClubRep/", allShowingsClubRep, name='movieShowingsClubRep'),
    
 #   path("bookMovieShowingClubRep/<screening_id>", bookShowingClubRep, name='bookMovieShowingClubRep'),
    #path('login/', login_view, name="login"),
    #path('logout/', logout_view, name="logout"),
    #path('register/', register_view, name="register"),
    
] 