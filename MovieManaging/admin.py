from django.contrib import admin
from MovieManaging.models import *

class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(movieListing)
admin.site.register(addNewScreen)
admin.site.register(movieTimeSlots)
admin.site.register(pickMovie)