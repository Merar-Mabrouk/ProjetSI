from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('achat/',views.add_achat)
]