# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .data import *
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
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
    else:
        form=ClientForm()
        msg="add a client"
        return render(request,"Client.html",{'form':form,'Message':msg})
            
def menu(request):
    user = request.user
    user_groups = user.groups.all()
    if user_groups.exists():
        first_group = user_groups.first()
    else:
        first_group = None
    print('hna el wasmou:'+str(first_group))
    return render(request,"index.html",{'group':str(first_group)})

def identify(request):
    return redirect('login')

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
            msg="something wrong with the form"
            return render(request,"Raw.html",{'form':form,'Message':msg})
    else:
        form=RawForm()
        msg="add a Material"
        return render(request,"Raw.html",{'form':form,'Message':msg})

def add_achat(request):
    print('our request is: '+str(request))
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
    clients = Client.objects.all()
    RawMaterials = RawMaterial.objects.all()
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            idM = form.cleaned_data['matiere']
            caseM = "remove"
            quant = form.cleaned_data['quantity']
            if modify_raw_by_id(idM=idM, case=caseM, count=quant):
                idS = form.cleaned_data['client']
                reg = form.cleaned_data['p_credits']
                regler_client(pk=idS, somme=reg, cond='add')
                form.save()
                form = VenteForm()
                msg = "The new Vente is successfully added"
            else:
                msg = "The quantity you are trying to sell is superior to what you have"
            return render(request,"vente.html",{'form':form,'Message':msg,'clients':Client,'Raw':RawMaterials})
        else:
            form=VenteForm()
            msg="ur form is invalid"
            return render(request,"vente.html",{'form':form,'Message':msg,'clients':Client,'Raw':RawMaterials})
    else:
        form=VenteForm()
        msg="add a Vente"
        return render(request,"vente.html",{'form':form,'Message':msg,'clients':Client,'Raw':RawMaterials})
def add_transfer(request):
    centres=Centre.objects.all()
    RawMaterials=RawMaterial.objects.all()
    if(request.method =='POST'):
        form=TransferForm(request.POST)
        if form.is_valid():
            idM=form.cleaned_data['matiere']
            caseM="remove"
            quant=form.cleaned_data['quantity']
            if(modify_raw_by_id(idM=idM,case=caseM,count=quant)):
                form.save()
                form=TransferForm()
                msg="the new Vente is successfully added"
            else:
                form=TransferForm()
                msg="the quantity u are trying to transfer is superior to what u have"                    
            return render(request,"transfer.html",{'form':form,'Message':msg,'center':centres,'Raw':RawMaterials})
        else:
            form=TransferForm()
            msg="add a transfer"
            return render(request,"transfer.html",{'form':form,'Message':msg,'center':centres,'Raw':RawMaterials})
    else:
        form=TransferForm()
        msg="add a transfer"
        return render(request,"transfer.html",{'form':form,'Message':msg,'center':centres,'Raw':RawMaterials}) 
        


### here are the modifications ###
def modify_client(request,pk):
    client=Client.objects.get(id=pk)
    if(request.method=='POST'):
        form=ClientForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            return redirect(listClient)
    else:
        form=ClientForm()        
        return render(request,"clientM.html",{'form':form,})


def modify_supplier(request,pk):
    supp=Supplier.objects.get(id=pk)
    if(request=='POST'):
        form=SupplierForm(request.POST,instance=supp)
        if form.is_valid():
            form.save()
            return redirect(listSupplier)
    else:
        form=ClientForm()        
        return render(request,modifySupplier,{'form':form,})
    

def modify_achat(request, pk):
    achat = Achat.objects.get(id=pk)
    
    if request.method == 'POST':
        form = AchatForm(request.POST, instance=achat)
        if form.is_valid():
            form.save()
            return redirect('list_achats')  # Replace with the actual URL for listing achats
    else:
        form = AchatForm(instance=achat)
        
    return render(request, "achat.html", {'form': form})

def modify_vente(request, pk):
    vente = Vente.objects.get(num_vente=pk)
    
    if request.method == 'POST':
        form = VenteForm(request.POST, instance=vente)
        if form.is_valid():
            form.save()
            return redirect('list_ventes')  # Assuming you have a URL named 'list_ventes' for listing ventes
    else:
        form = VenteForm(instance=vente)
        
    return render(request, "venteM.html", {'form': form})

def modify_transfer(request, pk):
    transfer = Transfer.objects.get(num_tr=pk)
    
    if request.method == 'POST':
        form = TransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return redirect('list_transfers')  # Assuming you have a URL named 'list_transfers' for listing transfers
    else:
        form = TransferForm(instance=transfer)
        
    return render(request, "transferM.html", {'form': form})
###   ###    
def regler_vente(request,pk):
    vente=Vente.objects.get(id=pk)
    if(request.method=='POST'):
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
    if(request.method=='POST'):
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
    else:
        form=AchatRForm()
        msg="regler l'Achat"
        return render(request,regletAchat,{'form':form, 'achat':achat})
        
        
        
    
### here u find the views that are used by the  center###    

def add_product(request):
    if(request.method=='POST'):
        form=ProductForm(request.POST,instance=Product)
        if(form.is_valid):
            msg="The product was added successfully"
            form.save()
            return render(request,addProduct,{'form':form})
        else :
            msg="add a product "
            form=ProductForm()
            return render(request,addProduct,{'form':form})
        
    else :
        msg="add a product "
        form=ProductForm()
        return render(request,addProduct,{'form':form})

def add_VenteP(request):
    print('our request is: '+str(request)) 
    RawMaterials=Product.objects.all()
    clients=Client.objects.all()
    if request.method == 'POST':
        form=VentePForm(request.POST)
        if form.is_valid():
            idM=form.cleaned_data['code_p']
            print('our idm is'+ idM.Desiginiation_P)
            caseM="remove"
            quant=form.cleaned_data['quantity']
            if(modify_product_by_id(idM=idM,case=caseM,count=quant)):
                idS=form.cleaned_data['code_cl']
                reg=form.cleaned_data['p_credits']
                regler_client(pk=idS,somme=reg,cond='add')
                form.save()
                form = VentePForm()
                msg = "The new Vente Product is successfully added"
            else:
                msg = "The quantity you are trying to sell is superior to what you have"

        else:
            form = VentePForm()
            msg = "The form is invalid"

    else:
        form = VentePForm()
        msg = "Add a Vente for a product"

    return render(request, 'vente_p.html', {'form': form, 'Message': msg, 'clients': clients, 'Raw': RawMaterials})


def regler_venteP(request,pk):
    vente=VenteP.objects.get(id=pk)
    if(request.method=='POST'):
        form=VenteRForm(request.POST,instance=vente)
        if form.is_valid():
            cred=form.cleaned_data['p_credits']
            if(vente.p_credits<cred):
                msg="the money added is too much"
                form=VenteRForm()
                return render(request,regletVenteP,{'form':form, 'vente':vente})
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
    else:
        form=VenteRForm()
        msg="regler la vente"
        return render(request,regletVente,{'form':form, 'vente':vente})    
       
def add_Massrouf(request):
    employe=Employe.objects.all()
    if(request.method=='POST'):
        form=MassroufForm(request.POST,instance=Massrouf)
        if form.is_valid():
            cred=form.cleaned_data['Credit']
            em=form.cleaned_data['fk_Code']
            if(cred>em.Salaire_par_jour):
                msg="u can't give him more than he earn.."
                form=MassroufForm()
                return render(request,masrouf,{'form':form,'Message':msg,'employee':employe})
            else:
                form.save()
                msg="success"
                return render(request,masrouf,{'form':form,'Message':msg,'employee':employe})
    else:
        form=MassroufForm()
        msg="add Massrouf"            
        return render(request,masrouf,{'form':form,'Message':msg,'employee':employe})
        
        
def add_pointage(request):
    if(request.method=='POST'):
        form=PointageForm(request.POST,instance=Pointage)
        if form.is_valid():
            em=form.cleaned_data['Employe']
            date=form.cleaned_data['Date_P']
            p=Pointage.objects.filter(Employee=em,Date_P=date).exists()
            if(p):
                msg='you already have the pointage'
                form=PointageForm()
                return render(request,Pointage,{'form':form,'Message':msg})
            else:
                msg='you are registered in'
                form.save()
                form=PointageForm()
                return render(request,Pointage,{'form':form,'Message':msg})
        else:
            msg='you are not registered, something is wrong'
            form=PointageForm()
            return render(request,Pointage,{'form':form,'Message':msg})            
    else:
        msg="register in"    
        form=PointageForm()
        return render(request,Pointage,{'form':form,'Message':msg})

###  here you can find the list of everything ###
def list_achats(request):
    achats=Achat.objects.all()
    return render(request,listAchat,{'achats':achats})
def list_prod(request):
    produits=Product.object.all()
    return render(request,listProd,{'prods':produits})
def list_raw(request):
    raw=RawMaterial.objects.all()
    return render(request,listRaw,{'raws':raw})
def list_transfer(request):
    Trs=Transfer.objects.all()
    return render(request,listTransfer,{'Trs':Trs})
def list_vente(request):
    ventes=Vente.objects.all()    
    return render(request,listVente,{'ventes':ventes})

def list_VenteP(request):
    ventes=VenteP.objects.all()
    return render(request,listVenteP,{'ventes':ventes})

def list_reglementV(request):
    ventes=Vente.objects.filter(p_credits__gt=0)
    return render(request,listVenteR,{'ventes':ventes})

def list_reglementP(request):
    ventes=VenteP.objects.filter(p_credits__gt=0)
    return render(request,listVentePR,{'ventes':ventes})

def list_reglementA(request):
    achats=Achat.objects.filter(reglement__gt=0)
    return render(request,listRegleA,{'achats':achats})

    
        


### here u find the deleting stuff ###    
            
def delete_achat(request, pk):
    achat = Achat.objects.get(id=pk)
    
    if request.method == 'POST':
        achat.delete() 
        return redirect('list_achats')  # Replace with the actual URL for listing achats
    
    return render(request, "achat_delete.html", {'achat': achat})          
            
def delete_client(request, pk):
    client = Client.objects.get(id=pk)
    
    if request.method == 'POST':
        client.delete()
        return redirect('list_clients')  # Assuming you have a URL named 'list_clients' for listing clients
    
    return render(request, "client_delete.html", {'client': client})   

def delete_transfer(request, pk):
    transfer = Transfer.objects.get(num_tr=pk)
    
    if request.method == 'POST':
        transfer.delete()
        return redirect('list_transfers')  # Assuming you have a URL named 'list_transfers' for listing transfers
    
    return render(request, "transfer_delete.html", {'transfer': transfer})

def delete_product(request, pk):
    product = Product.objects.get(Code_P=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('list_products')  # Assuming you have a URL named 'list_products' for listing products
    
    return render(request, "product_delete.html", {'product': product})         
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

def modify_product_by_id(idM, case, count):
    counts = int(count)
    if(case == "add"):
        idM.Quantity=idM.Quantity+counts
    else:
        if(idM.Quantity<counts):
            return False
        idM.Quantity= idM.Quantity - counts
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

@require_GET
def get_clients(request):
    term = request.GET.get('q', '')
    # Perform a query to retrieve suppliers based on the search term
    # Replace the following line with your actual query logic
    clients = Client.objects.filter(first_name__icontains=term)
    data = [{'id': client.id, 'text': str(client)} for client in clients]
    return JsonResponse(data, safe=False)

@require_GET
def get_Products(request):
    term = request.GET.get('q', '')
    products = Product.objects.filter(Desiginiation_P__icontains=term)
    data = [{'id': product.Code_P, 'text': str(product)} for product in products]
    return JsonResponse(data, safe=False)
