    
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
    
    
    