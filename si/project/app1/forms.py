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
        fields=['centre','matiere','quantity']
        
        
class AchatRForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['reglement']
        
class VenteRForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['p_credits']