from django.urls import path
from . import views

app_name = "ticketmachine"
urlpatterns = [
    path("", views.index, name="index"),
    path("planning", views.planning, name="planning"),
    path("payment", views.payment, name="payment"),
]