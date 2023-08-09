from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    rating = models.FloatField(default=0.0)
    watchlist = models.ManyToManyField('AuctionListing', related_name='watchers', blank=True)
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_bid = models.FloatField()
    current_bid = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    bid_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f" Bid by {self.bidder.username} on {self.listing.title} for {self.amount}"

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Comment by {self.commenter.username} on {self.listing.title } : {self.text}"

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
    listings = models.ManyToManyField(AuctionListing)
