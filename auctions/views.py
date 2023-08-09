from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import AuctionListingForm
from .models import Category, User, AuctionListing

def index(request):
    return render(request, "auctions/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='auctions/login.html')
def create(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AuctionListingForm(user = request.user)

    return render(request, 'auctions/create.html', {'form': form})


def category(request):
    category = Category.objects.all()
    return render(request, 'auctions/category.html', {'categories': category})

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listing = AuctionListing.objects.filter(category=category)
    return render(request, 'auctions/category_detail.html', {'category':category, 'listings': listing})
