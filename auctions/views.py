from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, Listing, Bids, Comments, Watchlist, Closed


def index(request):
    #query db for infos
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def auctions(request, title):
    if request.method == "POST":
        # get the current "winner"
        listing = Listing.objects.get(title=title)
        heighest_bid = listing.heighest_bid

        bids = Bids.objects.get(bid=heighest_bid)
        winner = bids.username

        try:
            watchlist = Watchlist.objects.get(listing_title=title, username=request.user.username)

        except:
            watchlist = None
   
        # getting posted comment
        if request.POST["comment"]:
            comments = Comments()
            comments.username = request.user.username
            comments.listing_title = title
            comments.comment = request.POST["comment"] 
            comments.time = datetime.datetime.now()
         
        if comments.comment == "":
            return render(request, "auctions/auctions.html", {
                "title": title,
                "listings": Listing.objects.filter(title=title),
                "message": "Please, provide a valid comment",
                "class": "alert alert-danger",
                "comment": Comments.objects.filter(listing_title=title),
                "winner": winner,
                "watchlist": watchlist
            })
        
        else:
            # saving comment
            comments.save()

        return render(request, "auctions/auctions.html", {
            "title": title,
            "listings": Listing.objects.filter(title=title),
            "comment": Comments.objects.filter(listing_title=title),
            "winner": winner,
            "watchlist": watchlist
        })

    else:
        creatorid = Listing.objects.filter(title=title)[0]
        id = creatorid.creator_id
        creator = User.objects.filter(id=id)
        creator = creator[0]

        title = title
        comment = Comments.objects.filter(listing_title=title)
        try:
            watchlist = Watchlist.objects.get(listing_title=title, username=request.user.username)
        except:
            watchlist = None

        try:
            # get the current "winner"
            listing = Listing.objects.get(title=title)
            heighest_bid = listing.heighest_bid

            bids = Bids.objects.get(bid=heighest_bid)
            winner = bids.username
        except:
            winner = ""

        return render(request, "auctions/auctions.html", {
            "title": title,
            "listings": Listing.objects.filter(title=title),
            "comment": comment,
            "winner": winner,
            "watchlist": watchlist,
            "creator": creator
        })


def bid(request, title):
    if request.method == "POST":
        bids = Bids()
        # get posted form
        bids.username = request.user.username
        bids.listing_title = title
        bids.bid = int(request.POST["bid"])

        try:
            watchlist = Watchlist.objects.get(listing_title=title, username=request.user.username)
        except:
            watchlist = None

        # check if there already is a bid
        if Listing.objects.get(title=title).heighest_bid:
            currentbid = Listing.objects.get(title=title)
            if bids.bid > int(currentbid.heighest_bid):
                # update heighest_bid
                currentbid.heighest_bid = bids.bid
                currentbid.save()
                # saving bid 
                bids.save()
                message = "Succesfull bid!"
                clas = "alert alert-success" 
            else:
                message = "Bid must be greater than heighest bid"
                clas = "alert alert-warning" 
        else:
            currentbid = Listing.objects.get(title=title)
            if bids.bid > currentbid.price:
                # update heighest_bid
                currentbid.heighest_bid = bids.bid
                currentbid.save()
                # saving bid 
                bids.save()
                message = "Succesfull bid!"
                clas = "alert alert-success"
            else:
                message = "Bid must be greater than current price"
                clas = "alert alert-warning" 

        try:
            # get the current "winner"
            listing = Listing.objects.get(title=title)
            heighest_bid = listing.heighest_bid

            bids = Bids.objects.get(bid=heighest_bid)
            winner = bids.username
        except:
            winner = ""
        return render(request, "auctions/auctions.html", {
                "title": title,
                "listings": Listing.objects.filter(title=title),
                "comment": Comments.objects.filter(listing_title=title),
                "message": message,
                "class": clas,
                "winner": winner,
                "watchlist": watchlist
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


def create_listing(request):
    if request.method == "POST":
        # get posted content
        nulo = ""
        listing = Listing()
        
        listing.title = request.POST["title"]
        listing.price = request.POST["price"]
        listing.description = request.POST["description"]
        listing.category = request.POST["category"]
        listing.image = request.POST["image"]
        listing.creator_id = request.user.id
        listing.time = datetime.datetime.now()

        if listing.image == nulo:
            listing.image = "https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-1.jpg"
        
        if listing.title == nulo:
            return render(request, "auctions/create_listing.html", {
                "listings": Listing.objects.all(),
                "message": "Please, provide valid information",
                "class": "alert alert-danger"
            })
        try:
            # save into db
            listing.save()

        except ValueError:
            return render(request, "auctions/create_listing.html", {
                "listings": Listing.objects.all(),
                "message": "Please, provide valid information",
                "class": "alert alert-danger"
            })

        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
            "message": "Listing created succesfully",
            "class": "alert alert-success"
        })

    else:
        username = request.user.username
        user_id = request.user.id
        time = datetime.datetime.now()
        return render(request, "auctions/create_listing.html", {
            "username": username,
            "user_id": user_id,
            "time": time
        })


def watchlist(request, title):
    w = Watchlist()
    w.username = request.user.username
    w.listing_title = title

    w.save()
    
    # get the current "winner"
    listing = Listing.objects.get(title=title)
    heighest_bid = listing.heighest_bid

    bids = Bids.objects.get(bid=heighest_bid)
    winner = bids.username

    return render(request, "auctions/auctions.html", {
        "title": title,
        "listings": Listing.objects.filter(title=title),
        "comment": Comments.objects.filter(listing_title=title),
        "winner": winner,
        "message": "Listing successfully added to Watchlist",
        "class": "alert alert-success",
        "watchlist": "watchlist"
    })


def remove_watchlist(request, title):
    w = Watchlist.objects.get(username=request.user.username, listing_title=title)
    w.delete()
    
    # get the current "winner"
    listing = Listing.objects.get(title=title)
    heighest_bid = listing.heighest_bid

    bids = Bids.objects.get(bid=heighest_bid)
    winner = bids.username

    return render(request, "auctions/auctions.html", {
        "title": title,
        "listings": Listing.objects.filter(title=title),
        "comment": Comments.objects.filter(listing_title=title),
        "winner": winner,
        "message": "Listing successfully removed from Watchlist",
        "class": "alert alert-warning"
    })


def view_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(username=request.user.username)
    })


def close_bid(request, title):
    c = Closed()
    creator = Listing.objects.get(title=title)
    id = creator.creator_id
    creator = User.objects.get(id=id)
    
    # get the current "winner"
    try:
        listing = Listing.objects.get(title=title)
        heighest_bid = listing.heighest_bid
        bids = Bids.objects.get(bid=heighest_bid)
        winner = bids.username
        
    except:
        heighest_bid = listing.price
        winner = "None"

    c.creator = creator.username
    c.listing_title = title
    c.winner = winner
    c.price = listing.price
    c.image = listing.image
    c.description = listing.description
    c.category = listing.category
    c.winning_bid = listing.heighest_bid
    c.save()

    listing.delete()

    return render(request, "auctions/closed_bids.html", {
        "closed": Closed.objects.all(),
        "message": "Listing successfully closed",
        "class": "alert alert-success"
    })


def closed_bids(request):
    return render(request, "auctions/closed_bids.html", {
        "closed": Closed.objects.all()
    })


def closed_view(request, title):
    return render(request, "auctions/closed_view.html", {
        "closed": Closed.objects.filter(listing_title=title),
        "comment": Comments.objects.filter(listing_title=title)
    })


def search(request):
    categories = Listing.objects.all()
    cat = []
    for c in categories:
        if c.category not in cat:
            cat.append(c.category)
    return render(request, "auctions/categories.html", {
        "categories": cat
    })


def search_category(request, category):
    listing = Listing.objects.filter(category=category)

    return render(request, "auctions/search.html", {
        "listing": listing
    })