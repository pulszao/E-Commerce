from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<str:title>", views.auctions, name="auctions"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("watchlist/<str:title>", views.watchlist, name="watchlist"),
    path("remove_watchlist/<str:title>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("create_listing", views.create_listing, name="create"),
    path("closed_bids", views.closed_bids, name="closed_bids"),
    path("close_bid/<str:title>", views.close_bid, name="close_bid"),
    path("closed_bid/<str:title>", views.closed_view, name="close_view")
]
