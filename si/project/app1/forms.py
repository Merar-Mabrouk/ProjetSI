from django import forms
from .models import *


class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = "__all__"
        
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = "__all__"
        
class RawForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = '__all__'
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        
class TransferForm(forms.ModelForm):
    class Meta:
        model= Transfer
        fields='__all__'
        
        
class AchatRForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['reglement']
        
class VenteRForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['p_credits']