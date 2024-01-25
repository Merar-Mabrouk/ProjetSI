from django import forms
from .models import *


class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['supplier', 'matiere', 'quantity', 'unit_price', 'reglement']
        
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['quantity','prix_U','p_credits','client','matiere']
        
class RawForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ['designation','Qstock']
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name','last_name','address','phone','credit']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['first_name','last_name','address','phone','balance']
        
class TransferForm(forms.ModelForm):
    class Meta:
        model= Transfer
        fields=['centre','matiere','quantity','prix_Unit']
        
        
class AchatRForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['reglement','supplier']
        
class VenteRForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['p_credits','client']
          
###  here the things used in the centres  ###
class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields= ['Desiginiation_P','Quantity']
        
class VentePForm(forms.ModelForm):
    class Meta:
        model= VenteP
        fields=['quantity','prix_Unit','p_credits','code_cl','code_p']

class PointageForm(forms.ModelForm):
     class Meta:
         model= Pointage
         fields=['Date_P','Pointe','Employe']
         
class MassroufForm(forms.ModelForm):
    class Meta:
        model= Massrouf
        fields=['Date_M','Credit','fk_Code']