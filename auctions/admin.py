from django.contrib import admin
from .models import User, Listing, Bids, Comments, Watchlist, Closed

# Register your models here.
    #adding db into django admin interface
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Closed)