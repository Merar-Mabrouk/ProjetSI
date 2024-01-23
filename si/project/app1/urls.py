from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('',views.identify),
    path('menu/',views.menu,name='menu'),
    path('achat/',views.add_achat,name="achat"),
    path('vente/',views.add_vente,name="vente"),
    path('transfer/',views.add_transfer,name="transfer"),
    path('vente_p/',views.add_VenteP,name="vprod"),
    path('your-suppliers-endpoint/', views.get_suppliers, name='get_suppliers'),
    path('your-clients-endpoint/', views.get_clients, name='get_clients'),
    path('your-raw-materials-endpoint/', views.get_raw_materials, name='get_raw_materials'),
    path('your-product-endpoint/', views.get_Products, name='get_product'),
    path('add_supplier', views.add_supplier, name='add_supplier'),
]

