from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("flight-offers-search", views.verify, name="requests")
]