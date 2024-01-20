# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .data import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
def add_client(request):
    if(request.method =='POST'):
        form=ClientForm(request.POST)
        
        if form.is_valid():
            form.save()
            form=ClientForm()
            msg="the new client is successfully added"
            return render(request,"Client.html",{'form':form,'Message':msg})
        else:
            form=ClientForm()
            msg="add a client"
            return render(request,"Client.html",{'form':form,'Message':msg})
            
def add_supplier(request):
    if(request.method =='POST'):
        form=SupplierForm(request.POST)
        
        if form.is_valid():
            form.save()
            form=SupplierForm()
            msg="the new Supplier is successfully added"
            return render(request,"Supplier.html",{'form':form,'Message':msg})
        else:
            form=SupplierForm()
            msg="add a Supplier"
            return render(request,"Supplier.html",{'form':form,'Message':msg})
def add_rawMaterial(request):
    if(request.method =='POST'):
        form=RawForm(request.POST)
        
        if form.is_valid():
            form.save()
            form=RawForm()
            msg="the new Material is successfully added"
            return render(request,"Raw.html",{'form':form,'Message':msg})
        else:
            form=RawForm()
            msg="add a Material"
            return render(request,"Raw.html",{'form':form,'Message':msg})

def add_achat(request):
    suppliers=Supplier.objects.all()
    RawMaterials=RawMaterial.objects.all()
    if(request.method =='POST'):
        form=AchatForm(request.POST)
        if form.is_valid():
            # Manually process 'supplier' and 'matiere' fields
            try:
                supplier_id = request.POST.get('supplier')
                supplier = Supplier.objects.get(id=supplier_id)
                form.instance.supplier = supplier

                matiere_id = request.POST.get('matiere')
                matiere = RawMaterial.objects.get(id=matiere_id)
                form.instance.matiere = matiere
            except ObjectDoesNotExist:
                form.add_error(None, 'Invalid supplier or raw material')
                return render(request,"achat.html",{'form':form,'Message':'Invalid supplier or raw material','supp':suppliers,'Raw':RawMaterials})

            form.save()
            idM=form.cleaned_data['matiere']
            caseM="add"
            quant=form.cleaned_data['quantity']
            modify_raw_by_id(idM=idM,case=caseM,count=quant)
            idS=form.cleaned_data['supplier']
            reg=form.cleaned_data['reglement']
            regler_supplier(pk=idS,somme=reg,cond='add')
            form=AchatForm()
            msg="the new transaction is successfully added"
            return render(request,"achat.html",{'form':form,'Message':msg,'supp':suppliers,'Raw':RawMaterials})
        else:
            form=AchatForm()
            msg="add a transaction"
            return render(request,"achat.html",{'form':form,'Message':msg,'supp':suppliers,'Raw':RawMaterials})
    else: 
        form=AchatForm()
        msg="add a transaction"
        return render(request,"achat.html",{'form':form,'Message':msg,'supp':suppliers,'Raw':RawMaterials})
def add_vente(request):
    if(request.method =='POST'):
        form=VenteForm(request.POST)
        clients=Client.objects.all()
        RawMaterials=RawMaterial.objects.all()
        if form.is_valid():
            idM=form.cleaned_data['matiere']
            caseM="remove"
            quant=form.cleaned_data['quantity']
            if(modify_raw_by_id(idM=idM,case=caseM,quant=quant)):
                idS=form.cleaned_data['client']
                reg=form.cleaned_data['p_credits']
                regler_client(pk=idS,somme=reg,cond='add')
                form.save()
                form=TransferForm()
                msg="the new Vente is successfully added"
            else:
                msg="the quantity u are trying to sell is superior to what u have"  
            return render(request,"vente.html",{'form':form,'Message':msg,'clients':Client,'Raw':RawMaterials})
        else:
            form=VenteForm()
            msg="add a Vente"
            return render(request,"vente.html",{'form':form,'Message':msg,'clients':Client,'Raw':RawMaterials})
def add_transfer(request):
    if(request.method =='POST'):
        form=TransferForm(request.POST)
        centres=Centre.objects.all()
        RawMaterials=RawMaterial.objects.all()
        if form.is_valid():
            idM=form.cleaned_data['matiere']
            caseM="remove"
            quant=form.cleaned_data['quantity']
            if(modify_raw_by_id(idM=idM,case=caseM,quant=quant)):
                form.save()
                form=TransferForm()
                msg="the new Vente is successfully added"
            else:
                msg="the quantity u are trying to transfer is superior to what u have"                    
            return render(request,"transfer.html",{'form':form,'Message':msg,'center':centres,'Raw':RawMaterials})
        else:
            form=TransferForm()
            msg="add a Vente"
            return render(request,"transfer.html",{'form':form,'Message':msg,'center':centres,'Raw':RawMaterials})


### here are the modifications ###
def modify_client(request,pk):
    client=Client.objects.get(id=pk)
    if(request=='POST'):
        form=clientForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            return redirect(listClient)
    else:
        form=ClientForm()        
        return render(request,"clientM.html",{'form':form,})
    
def modify_supplier(request,pk):
    supp=Supplier.objects.get(id=pk)
    if(request=='POST'):
        form=suppForm(request.POST,instance=supp)
        if form.is_valid():
            form.save()
            return redirect(listSupplier)
    else:
        form=ClientForm()        
        return render(request,modifySupplier,{'form':form,})
    
def regler_vente(request,pk):
    vente=Vente.objects.get(id=pk)
    if(request=='POST'):
        form=VenteRForm(request.POST,instance=vente)
        if form.is_valid():
            cred=form.cleaned_data['p_credits']
            if(vente.p_credits<cred):
                msg="the money added is too much"
                form=VenteRForm()
                return render(request,regletVente,{'form':form, 'vente':vente})
            else:
                idS=form.cleaned_data['client']
                reg=form.cleaned_data['p_credits']
                regler_supplier(pk=idS,somme=reg,cond='regler')
                form.save()
                msg="the cut was added successfully"
                return redirect(listVente)
                
        else:
            form=VenteRForm()
            msg="regler la vente"
            return render(request,regletVente,{'form':form, 'vente':vente})
    
def regler_Achat(request,pk):
    achat=Achat.objects.get(id=pk)
    if(request=='POST'):
        form=AchatRForm(request.POST,instance=achat)
        if form.is_valid():
            cred=form.cleaned_data['reglement']
            if(achat.reglement<cred):
                msg="the money added is too much"
                form=AchatRForm()
                return render(request,regletAchat,{'form':form, 'achat':achat})
            else:
                form.save()
                idS=form.cleaned_data['supplier']
                reg=form.cleaned_data['reglement']
                regler_supplier(pk=idS,somme=reg,cond='regler')
                msg="the cut was added successfully"
                return redirect(listAchat)
                
        else:
            form=AchatRForm()
            msg="regler l'Achat"
            return render(request,regletAchat,{'form':form, 'achat':achat})
    
### here u find the deleting stuff ###    
            
### here we find functions that are to be used in other one.. ###            

def regler_client(pk, somme, cond):
    client=pk
    if cond=="regler":
        client.credit=client.credit-somme
    else:
        client.credit=client.credit+somme
    client.save()
    return True

def regler_supplier(pk, somme, cond):
    supplier=pk
    if cond=="regler":
        supplier.balance=supplier.balance-somme
    else:
        supplier.balance=supplier.balance+somme
    supplier.save()
    return True

def modify_raw_by_id(idM, case,count):
    counts=int(count)
    if(case == "add"):
        idM.Qstock= idM.Qstock+ counts
    else:
        if(idM.Qstock<counts):
            return False
        idM.Qstock= idM.Qstock - counts
    idM.save()
    return True

        
        
            
            
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
 


@require_GET
def get_suppliers(request):
    term = request.GET.get('q', '')
    # Perform a query to retrieve suppliers based on the search term
    # Replace the following line with your actual query logic
    suppliers = Supplier.objects.filter(first_name__icontains=term)
    data = [{'id': supplier.id, 'text': str(supplier)} for supplier in suppliers]
    return JsonResponse(data, safe=False)

@require_GET
def get_raw_materials(request):
    term = request.GET.get('q', '')
    # Perform a query to retrieve raw materials based on the search term
    # Replace the following line with your actual query logic
    raw_materials = RawMaterial.objects.filter(designation__icontains=term)
    data = [{'id': raw_material.id, 'text': str(raw_material)} for raw_material in raw_materials]
    return JsonResponse(data, safe=False)
