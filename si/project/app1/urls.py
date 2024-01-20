from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('achat/',views.add_achat),
    path('your-suppliers-endpoint/', views.get_suppliers, name='get_suppliers'),
    path('your-raw-materials-endpoint/', views.get_raw_materials, name='get_raw_materials'),
]