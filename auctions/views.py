from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    #query db for infos
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def auctions(request, title):
    title = title
    return render(request, "auctions/auctions.html", {
        "title": title,
        "listings": Listing.objects.filter(title=title)
    })

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
                "class": "alert alert-danger",
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "class": "alert alert-warning",
        "message": "Logged out!"
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "class": "alert alert-danger",
                "message": "Passwords must match."
            })
        elif not password or not confirmation or not email:
            return render(request, "auctions/register.html", {
                "class": "alert alert-danger",
                "message": "Must fill all fields."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "class": "alert alert-danger",
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")