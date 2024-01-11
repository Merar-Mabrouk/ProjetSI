# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Supplier, Employee, RawMaterial, Achat, Sale, Stock, Centre

def add_entity(request, entity_type):
    if request.method == 'POST':
        # Handle the common form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Entity-specific handling
        if entity_type == 'client':
            credit = request.POST.get('credit')
            Client.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone,
                credit=credit
            )
        elif entity_type == 'supplier':
            balance = request.POST.get('balance')
            Supplier.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone,
                balance=balance
            )
        elif entity_type == 'employee':
            daily_salary = request.POST.get('daily_salary')
            centre_id = request.POST.get('centre')
            centre = Centre.objects.get(id=centre_id)
            Employee.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone=phone,
                daily_salary=daily_salary,
                centre=centre
            )
        elif entity_type == 'raw_material':
            RawMaterial.objects.create(
                name=first_name,
                code=last_name  # Assuming code is unique for raw materials
            )

        # Add more conditions for other entity types

        return redirect('entity_list_page')  # Redirect to the entity list page

    # Render the generic form template with entity_type and other necessary data
    centres = Centre.objects.all()
    return render(request, 'add_entity.html', {'entity_type': entity_type, 'centres': centres})

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