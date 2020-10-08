from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<str:title>", views.auctions, name="auctions"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("create_listing", views.create_listing, name="create")
]
