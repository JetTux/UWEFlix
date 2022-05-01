from django.contrib import admin

from accounts.models import studentClub, ClubRep, clubDetails

# Register your models here.
admin.site.register(studentClub)
admin.site.register(clubDetails)
admin.site.register(ClubRep)