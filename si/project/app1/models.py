    
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

# class Product(models.Model):
#     code = models.CharField(max_length=10, unique=True,auto_created=True)
#     designation = models.CharField(max_length=50,default=MATIERE_PREMIERE)
    
class RawMaterial(models.Model):
    codeM = models.CharField(max_length=10, unique=True)
    designation = models.CharField(max_length=50, )
    Qstock = models.IntegerField(max_length=10)    
    def __str__(self):
        return (self.designation)

class Client(models.Model):
    code_cl = models.CharField(max_length=10, unique=True,auto_created=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField()
    credit = models.FloatField()
    def __str__(self):
        return self.last_name+' '+self.first_name

class Supplier(models.Model):
    code_S = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=40, )
    last_name = models.CharField(max_length=40, unique=True)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField()
    balance = models.FloatField()
    def __str__(self):
        return (self.first_name + ' ' + self.last_name)
class Centre(models.Model):
    code = models.CharField(max_length=10, unique=True)
    designation = models.CharField(max_length=50)
    def __str__(self):
        return (self.designation)

class Employee(models.Model):
    code = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField()
    daily_salary = models.FloatField()
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)
    def __str__(self):
        return self.first_name+''+self.last_name

class Achat(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    matiere = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    reglement = models.FloatField()
    def __str__(self):
        return ("l'achat num"+self.id)

class Transfer(models.Model):
    num_tr=models.CharField(auto_created=True, max_length=10,null=False,editable=False)
    date = models.DateTimeField(auto_now_add=True,unique=True)
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)
    matiere = models.ForeignKey(RawMaterial,on_delete=models.CASCADE)
    prix_Unit=models.FloatField()
    quantity = models.IntegerField()
    def __str__(self):
        return ('Transfer num'+self.num_tr)

class Vente(models.Model):
    num_vente=models.IntegerField(primary_key=True, auto_created=True, unique=True, editable=False)
    sale=models.CharField(auto_created=True, max_length=10)
    quantity=models.IntegerField(max_length=10)
    prix_U=models.FloatField()
    p_credits=models.FloatField()
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    matiere=models.ForeignKey(RawMaterial,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return ('vente num'+str(self.num_vente))
    
    
class Stock(models.Model):
    code=models.CharField(max_length=10,unique=True,auto_created=True)
    name_P=models.ForeignKey(RawMaterial,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def __str__(self):
        return self.name_p
    
# class ReglementAchat(models.Model):
#     code=models.CharField(max_length=10,unique=True,auto_created=True)
#     numA=models.ForeignKey(Achat)
#     rigli=models.BooleanField(default=False)
#     restant=models.FloatField(max_length=10,null=False)
class Product(models.Model):
    Code_P=models.CharField(max_length=10,null=False,auto_created=True)
    Desiginiation_P=models.CharField(max_length=10)
    Quantity=models.IntegerField()
    prix_Unit=models.IntegerField() 
    def __str__(self):
        return self.Desiginiation_P

class VenteP(models.Model):
    num_V=models.IntegerField()
    Date_v=models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField()
    prix_Unit=models.FloatField()
    p_credits=models.FloatField()
    code_cl=models.ForeignKey(Client,on_delete=models.CASCADE)
    code_p=models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return "Vente num"+self.num_V

class Employe(models.Model):
    Code_E = models.CharField(max_length=20, primary_key=True)
    Nom_E = models.CharField(max_length=100)
    Prenom_E = models.CharField(max_length=100)
    Adresse_E = models.CharField(max_length=200)
    Tel_E = models.CharField(max_length=15)
    Salaire_par_jour = models.DecimalField(max_digits=10, decimal_places=2)
    fk_Code_CE = models.CharField(max_length=20)  # Assurez-vous que le type correspond au type de la clé étrangère dans votre modèle Code_CE
    def __str__(self):
        return self.Nom_E+' '+self.Prenom_E
    
class PV(models.Model):
    Date_PV = models.DateTimeField(primary_key=True)
    Text = models.TextField()
    def __str__(self):
        return str(self.Date_PV.now())

class EnRapport(models.Model):
    fk_Code_E = models.ForeignKey(Employe, on_delete=models.CASCADE)
    fk_Date_PV = models.ForeignKey(PV, on_delete=models.CASCADE)
    def __str__(self):
        return 'en rapport avec'+self.fk_Code_E

class Pointage(models.Model):
    Num_P = models.AutoField(primary_key=True)
    Date_P = models.DateTimeField()
    Pointe = models.BooleanField()
    Employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    def __str__(self):
        return 'Pointage:'+self.Num_P+' de '+self.Employe.name_E
    

class Massrouf(models.Model):
    Num_MAS = models.AutoField(primary_key=True)
    Date_M = models.DateTimeField()
    Credit = models.DecimalField(max_digits=10, decimal_places=2)
    fk_Code = models.ForeignKey(Employe, on_delete=models.CASCADE)
    def __str__(self):
        return self.Num_MAS
    
  