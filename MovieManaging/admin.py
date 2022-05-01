from django.contrib import admin
#from accounts.models import Account
from MovieManaging.models import *

class AuthorAdmin(admin.ModelAdmin):
    pass

##admin.site.register(Account)
admin.site.register(movieListing)
admin.site.register(addNewScreen)
admin.site.register(movieTimeSlots)
admin.site.register(pickMovie)