    
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# class Product(models.Model):
#     code = models.CharField(max_length=10, unique=True,auto_created=True)
#     designation = models.CharField(max_length=50,default=MATIERE_PREMIERE)
    
class RawMaterial(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)    

class Client(models.Model):
    code = models.CharField(max_length=10, unique=True,auto_created=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField()
    credit = models.FloatField()

class Supplier(models.Model):
    code = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField()
    balance = models.FloatField()

class Centre(models.Model):
    code = models.CharField(max_length=10, unique=True)
    designation = models.CharField(max_length=50)

class Employee(models.Model):
    code = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField()
    daily_salary = models.FloatField()
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)

class Achat(models.Model):
    pur=models.CharField(auto_created=True, max_length=10)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

class Transfer(models.Model):
    tr=models.CharField(auto_created=True, max_length=10)
    date = models.DateField(auto_now_add=True,unique=True)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    product = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Sale(models.Model):
    sale=models.CharField(auto_created=True, max_length=10)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ### TODO: verify if this is correct
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    
    
class Stock(models.Model):
    code=models.CharField(max_length=10,unique=True,auto_created=True)
    name_P=models.ForeignKey(RawMaterial,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def __str__(self):
        return self.name
    
class ReglementAchat(models.Model):
    code=models.CharField(max_length=10,unique=True,auto_created=True)
    numA=models.ForeignKey(Achat)
    rigli=models.BooleanField(default=False)
    restant=models.FloatField(max_length=10,null=False)
    
class Employe(models.Model):
    Code_E = models.CharField(max_length=20, primary_key=True)
    Nom_E = models.CharField(max_length=100)
    Prenom_E = models.CharField(max_length=100)
    Adresse_E = models.CharField(max_length=200)
    Tel_E = models.CharField(max_length=15)
    Salaire_par_jour = models.DecimalField(max_digits=10, decimal_places=2)
    fk_Code_CE = models.CharField(max_length=20)  # Assurez-vous que le type correspond au type de la clé étrangère dans votre modèle Code_CE

class PV(models.Model):
    Date_PV = models.DateField(primary_key=True)
    Text = models.TextField()

class EnRapport(models.Model):
    fk_Code_E = models.ForeignKey(Employe, on_delete=models.CASCADE)
    fk_Date_PV = models.ForeignKey(PV, on_delete=models.CASCADE)

class Doit(models.Model):
    fk_Code = models.CharField(max_length=20)
    fk_Num_P = models.IntegerField()

class Pointage(models.Model):
    Num_P = models.AutoField(primary_key=True)
    Date_P = models.DateField()
    Pointe = models.BooleanField()

class MASSROUF(models.Model):
    Num_MAS = models.AutoField(primary_key=True)
    Date_M = models.DateField()
    Credit = models.DecimalField(max_digits=10, decimal_places=2)
    fk_Code_E = models.ForeignKey(Employe, on_delete=models.CASCADE)