from django.urls import  path
from .views import *

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
    path("allShowings/", allShowingsForUpdating, name='allShowings'),
    path("updateShowings/<showing_id>", updateShowings, name='updateShowings'),
    path("requestCancellation/<booking_id>", requestCancellation, name='requestCancellation'),
    path("cancellationRequests/", cancellationRequests, name='cancellationRequests'),
    path('deleteBooking/<pickMovie_id>', deleteBooking, name='delete_booking'),
    path('deleteDiscount/<pickMovie_id>', deleteRequest, name='delete_request'),  
] 