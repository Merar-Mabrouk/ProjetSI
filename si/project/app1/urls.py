from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('',views.identify),
    path('menu/',views.menu,name='menu'),
    path('list_achat/',views.list_achats,name='listAchat'),
    path('list_achatR/',views.list_reglementA,name='listAchatR'),
    path('list_vente/',views.list_vente,name='listVente'),
    path('list_venteR/',views.list_reglementV,name='listVenteR'),
    path('list_raw/',views.list_raw,name='listRaw'),
    path('list_prod/',views.list_prod,name='listProd'),
    path('list_tr/',views.list_transfer,name='listTransfer'),
    path('list_ventP/',views.list_VenteP,name='listprodS'),
    path('list_ventPR/',views.list_reglementP,name='listVentePR'),
    path('achat/',views.add_achat,name="achat"),
    path('vente/',views.add_vente,name="vente"),
    path('transfer/',views.add_transfer,name="transfer"),
    path('vente_p/',views.add_VenteP,name="vprod"),
    path('your-suppliers-endpoint/', views.get_suppliers, name='get_suppliers'),
    path('your-clients-endpoint/', views.get_clients, name='get_clients'),
    path('your-raw-materials-endpoint/', views.get_raw_materials, name='get_raw_materials'),
    path('your-product-endpoint/', views.get_Products, name='get_product'),
    path('add_supplier', views.add_supplier, name='add_supplier'),
    # path('modify_achat/<int:pk>/', modify_achat, name='modify_achat'),
    # path('delete_achat/<int:pk>/', delete_achat, name='delete_achat'),
    
    # path('modify_transfer/<int:pk>/', modify_transfer, name='modify_transfer'),
    # path('delete_transfer/<int:pk>/', delete_transfer, name='delete_transfer'),
    
    # path('modify_vente/<int:pk>/', modify_vente, name='modify_vente'),
    # path('delete_vente/<int:pk>/', delete_vente, name='delete_vente'),
    
    # path('modify_product/<int:pk>/', modify_product, name='modify_product'),
    # path('delete_product/<int:pk>/', delete_product, name='delete_product'),
]

