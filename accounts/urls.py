from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('loginClubRep/', clubRepLogin, name='loginClubRep'),
    path('logout/', user_logout, name='logout'),
    path('accountList/', allAccounts, name='accountList'),
    path('viewClubRep/<clubRep_id>', notifyClubRep, name='viewClubRep'),
    path('viewClub/<studentClub_id>', viewClub, name='viewClub'),
    path("updateUser/<user_id>", updateUser, name='update_user'),
    path("updateClub/<studentClub_id>", updateClubAccount, name='update_club'),
    path("updateClubRep/<clubRep_id>", updateClubRep, name='update_club_rep'),
    path("createClubAccount/", createClubAccount, name="createClubAccount"),
    path("registerClub/", clubRegister, name="registerClub"),
    path("registerClubRep/", clubRepRegister, name="registerClubRep"),
    #New FV
    path('discountRequests/', discountRequests, name='discountRequests'),
    path('updateDiscount/<discountList_club>', updateDiscount, name='update_discount'),
    path('deleteDiscount/<discountList_id>', deleteDiscount, name='delete_discount'),
    path('requestDiscount/', requestDiscount, name='requestDiscount'),
]