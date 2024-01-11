from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Achat, Sale, Client, Supplier, RawMaterial, Employee

# Function to purchase a raw material
def purchase_raw_material(request):
    if request.method == 'POST':
        # Handle the form data and save the purchase record
        supplier_id = request.POST.get('supplier_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')

        supplier = Supplier.objects.get(id=supplier_id)
        product = RawMaterial.objects.get(id=product_id)

        Achat.objects.create(
            supplier=supplier,
            product=product,
            quantity=quantity,
            unit_price=unit_price
        )

        # Update stock or perform any other necessary actions

        return redirect('purchase_success_page')  # Redirect to a success page

    # Render the purchase form
    suppliers = Supplier.objects.all()
    products = RawMaterial.objects.all()
    return render(request, 'purchase_raw_material.html', {'suppliers': suppliers, 'products': products})

# Function to sell a raw material
def sell_raw_material(request):
    if request.method == 'POST':
        # Handle the form data and save the sale record
        client_id = request.POST.get('client_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')

        client = Client.objects.get(id=client_id)
        product = RawMaterial.objects.get(id=product_id)

        Sale.objects.create(
            client=client,
            product=product,
            quantity=quantity,
            unit_price=unit_price
        )

        # Update stock or perform any other necessary actions

        return redirect('sale_success_page')  # Redirect to a success page

    # Render the sale form
    clients = Client.objects.all()
    products = RawMaterial.objects.all()
    return render(request, 'sell_raw_material.html', {'clients': clients, 'products': products})

# Similarly, you can implement functions for other operations like adding/removing clients, suppliers, products, employees, etc.
# Don't forget to create corresponding HTML templates for the forms and success pages.
