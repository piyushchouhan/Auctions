from django.contrib import admin
from .models import User, AuctionListing, Comment, Bid, Category


admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(User)

