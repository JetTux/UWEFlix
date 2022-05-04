from django.urls import path
from accounts.views import *

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
    path('discountRequests/', discountRequests, name='discountRequests'),
    path('updateDiscount/<discountList_club>', updateDiscount, name='update_discount'),
    path('deleteDiscount/<discountList_id>', deleteDiscount, name='delete_discount'),
    path('requestDiscount/', requestDiscount, name='requestDiscount'),
    path('accountStatementList/', allAccountStatements, name='accountStatementList'),
    path('statementsYear/', statementsYear, name='statementsYear'),
    path('statementsMonth/', statementsMonth, name='statementsMonth'),
]