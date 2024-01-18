# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Supplier, Employee, RawMaterial, Achat, Sale, Stock, Centre
from .forms import *
def add_client(request):
    if(request.method =='POST'):
        form=ClientForm(request.POST)
        
        if form.is_valid():
            form.save()
            form=ClientForm()
            msg="the new client is successfully added"
            return render(request,"Client.html",{'form':form,'Message':message})
        else:
            form=ClientForm()
            msg="add a client"
            return render(request,"Client.html",{'form':form,'Message':message})
            
def add_supplier(request):
    if(request.method =='POST'):
        form=SupplierForm(request.POST)
        
        if form.is_valid():
            form.save()
            form=SupplierForm()
            msg="the new Supplier is successfully added"
            return render(request,"Supplier.html",{'form':form,'Message':message})
        else:
            form=SupplierForm()
            msg="add a Supplier"
            return render(request,"Supplier.html",{'form':form,'Message':message})
def add_rawMaterial(request):
    if(request.method =='POST'):
        form=RawForm(request.POST)
        
        if form.is_valid():
            form.save()
            form=RawForm()
            msg="the new Material is successfully added"
            return render(request,"Raw.html",{'form':form,'Message':message})
        else:
            form=RawForm()
            msg="add a Material"
            return render(request,"Raw.html",{'form':form,'Message':message})
def add_achat(request):
    if(request.method =='POST'):
        form=AchatForm(request.POST)
        clients=Client.objects.all()
        RawMaterials=RawMaterial.objects.all()
        if form.is_valid():
            form.save()
            form=AchatForm()
            msg="the new transaction is successfully added"
            return render(request,"achat.html",{'form':form,'Message':message,'clients':Client,'Raw':RawMaterials})
        else:
            form=AchatForm()
            msg="add a transaction"
            return render(request,"achat.html",{'form':form,'Message':message,'clients':Client,'Raw':RawMaterials})
def add_vente(request):
    if(request.method =='POST'):
        form=VenteForm(request.POST)
        clients=Client.objects.all()
        RawMaterials=RawMaterial.objects.all()
        if form.is_valid():
            form.save()
            form=VenteForm()
            msg="the new Vente is successfully added"
            return render(request,"vente.html",{'form':form,'Message':message,'clients':Client,'Raw':RawMaterials})
        else:
            form=VenteForm()
            msg="add a Vente"
            return render(request,"vente.html",{'form':form,'Message':message,'clients':Client,'Raw':RawMaterials})
def add_transfer(request):
    if(request.method =='POST'):
        form=TransferForm(request.POST)
        centres=Centre.objects.all()
        RawMaterials=RawMaterial.objects.all()
        if form.is_valid():
            form.save()
            form=TransferForm()
            msg="the new Vente is successfully added"
            return render(request,"transfer.html",{'form':form,'Message':message,'center':centres,'Raw':RawMaterials})
        else:
            form=TransferForm()
            msg="add a Vente"
            return render(request,"transfer.html",{'form':form,'Message':message,'center':centres,'Raw':RawMaterials})
        
def modify_entity(request, entity_type, entity_id):
    # Fetch the entity instance based on entity_type and entity_id
    model_class = {'client': Client, 'supplier': Supplier, 'employee': Employee, 'raw_material': RawMaterial}.get(entity_type, None)
    if not model_class:
        # Handle other entity types or raise an error as needed
        return HttpResponseBadRequest("Invalid entity type")

    entity = get_object_or_404(model_class, id=entity_id)

    if request.method == 'POST':
        # Handle modification
        # Similar to add_entity, update the fields based on entity_type

        entity.first_name = request.POST.get('first_name')
        entity.last_name = request.POST.get('last_name')
        entity.address = request.POST.get('address')
        entity.phone = request.POST.get('phone')

        if entity_type == 'client':
            entity.credit = request.POST.get('credit')
        elif entity_type == 'supplier':
            entity.balance = request.POST.get('balance')
        elif entity_type == 'employee':
            entity.daily_salary = request.POST.get('daily_salary')
            entity.centre_id = request.POST.get('centre')

        entity.save()

        return redirect('entity_list_page')  # Redirect to the entity list page

    # Render the generic form template with entity_type, entity_id, and other necessary data
    centres = Centre.objects.all()
    return render(request, 'modify_entity.html', {'entity_type': entity_type, 'entity': entity, 'centres': centres})

def delete_entity(request, entity_type, entity_id):
    # Fetch the entity instance based on entity_type and entity_id
    model_class = {'client': Client, 'supplier': Supplier, 'employee': Employee, 'raw_material': RawMaterial}.get(entity_type, None)
    if not model_class:
        # Handle other entity types or raise an error as needed
        return HttpResponseBadRequest("Invalid entity type")

    entity = get_object_or_404(model_class, id=entity_id)
    entity.delete()

    return redirect('entity_list_page')  # Redirect to the entity list page

# Function to purchase a raw material
def acheter_matiere_premiere(request):
    if request.method == 'POST':
        # Handle the form data and save the purchase record
        supplier_id = request.POST.get('supplier_id')
        raw_material_id = request.POST.get('raw_material_id')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')

        supplier = Supplier.objects.get(id=supplier_id)
        raw_material = RawMaterial.objects.get(id=raw_material_id)

        Achat.objects.create(
            supplier=supplier,
            product=raw_material,
            quantity=quantity,
            unit_price=unit_price
        )

        # Update stock or perform any other necessary actions
        stock, created = Stock.objects.get_or_create(name_P=raw_material)
        stock.quantity += int(quantity)
        stock.save()

        return redirect('purchase_success_page')  # Redirect to a success page

    # Render the purchase form
    suppliers = Supplier.objects.all()
    raw_materials = RawMaterial.objects.all()
    return render(request, 'acheter_matiere_premiere.html', {'suppliers': suppliers, 'raw_materials': raw_materials})

# Function to sell a raw material
def vendre_matiere_premiere(request):
    if request.method == 'POST':
        # Handle the form data and save the sale record
        client_id = request.POST.get('client_id')
        raw_material_id = request.POST.get('raw_material_id')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')

        client = Client.objects.get(id=client_id)
        raw_material = RawMaterial.objects.get(id=raw_material_id)

        Sale.objects.create(
            client=client,
            product=raw_material,
            quantity=quantity,
            unit_price=unit_price
        )

        # Update stock or perform any other necessary actions
        stock, created = Stock.objects.get_or_create(name_P=raw_material)
        stock.quantity -= int(quantity)
        stock.save()

        return redirect('sale_success_page')  # Redirect to a success page

    # Render the sale form
    clients = Client.objects.all()
    raw_materials = RawMaterial.objects.all()
    return render(request, 'vendre_matiere_premiere.html', {'clients': clients, 'raw_materials': raw_materials})