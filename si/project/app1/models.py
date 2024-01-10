from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Product(models.Model):
    code=models.CharField(max_length=10,auto_created=True)
    name=models.CharField(max_length=40)
    designation=models.CharField(max_length=10,choices= [
        (MATIERE_PREMIERE, 'Matière Première'),
        (UTILISER, 'Utiliser'),
    ],default=MATIERE_PREMIERE)
    nbrs=models.IntegerField(max_length=10)
    

class Client(models.Model):
    code=models.AutoField(max_length=10,auto_created=True)    
    name=models.CharField(max_length=40)
    pren=models.CharField(max_length=40)
    adr=models.CharField(max_length=40)
    phone=models= PhoneNumberField()
    credit=models.models.FloatField()
     
class Fournisseur(models.Model):
    code=models.AutoField(max_length=10,auto_created=True)    
    name=models.CharField(max_length=40)
    pren=models.CharField(max_length=40)
    adr=models.CharField(max_length=40)
    phone=models= PhoneNumberField()
    solde=models.models.FloatField()
    
class Centre(models.Model):
    code=models.AutoField(max_length=10,auto_created=True) 
    designation=models.IntegerField(choices= [
        (FIRST, 1),
        (SECOND, 2),
        (THREE, 3),
    ])
    
class Employe(models.Model):    
    code=models.AutoField(max_length=10,auto_created=True)    
    name=models.CharField(max_length=40)
    pren=models.CharField(max_length=40)
    adr=models.CharField(max_length=40)
    phone=models= PhoneNumberField()
    salaire=models.models.FloatField()
    Centre=models.ForeignKey(Centre, on_delete=models.CASCADE)
    
class achat(models.Model):
    code=models.AutoField(max_length=10,auto_created=True,unique=True)    
    date=models.DateField( auto_now=True, auto_now_add=True,)
         
         
