from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from auctions.models import User, AuctionListing, Watchlist
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@login_required(login_url='auctions/login.html')
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listings.add(listing)
    return JsonResponse({"message": "Added to watchlist"})

def checkIfItemInWatchlist(listing_id, user):
    # Try to fetch the user's watchlist
    user_watchlist = get_object_or_404(Watchlist, user=user)
    # Check if the AuctionListing with the given listing_id exists in the user's watchlist
    is_item_in_watchlist = user_watchlist.listings.filter(pk=listing_id).exists()
    return is_item_in_watchlist


def check_watchlist(request):
    listing_id = request.GET.get('listing_id')
    username = request.GET.get('username')
    
    user = User.objects.get(username=username)
    is_item_in_watchlist = checkIfItemInWatchlist(listing_id, user)

    return JsonResponse({'is_item_in_watchlist': is_item_in_watchlist})

@login_required(login_url='auctions/login.html')
def watchlist(request):
    try:
        user_watchlist = Watchlist.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # If the watchlist doesn't exist for the user, create a new one
        user_watchlist = Watchlist.objects.create(user=request.user)
    return render(request, 'watchlist/watchlist.html', {'user_watchlist': user_watchlist})
    
def remove_from_watchlist(request, listing_id):
    user_watchlist = Watchlist.objects.get(user=request.user)
    listing = AuctionListing.objects.get(pk=listing_id)
    user_watchlist.listings.remove(listing)
    return redirect('watchlist')




    

