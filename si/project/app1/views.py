from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Client, Supplier, RawMaterial, Employee
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

# Function to add a new client
def add_client(request):
    if request.method == 'POST':
        # Handle the form data and save the new client
        # Assuming you have a form with fields 'first_name', 'last_name', 'address', 'phone', 'credit'
        Client.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            credit=request.POST.get('credit')
        )
        return redirect('client_list_page')  # Redirect to the client list page

    # Render the form to add a new client
    return render(request, 'add_client.html')

# Function to remove a client
def remove_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
    return redirect('client_list_page')  # Redirect to the client list page

# Similar functions for adding/removing suppliers, products, employees, etc.

# Function to add a new supplier
def add_supplier(request):
    if request.method == 'POST':
        # Handle the form data and save the new supplier
        # Assuming you have a form with fields 'first_name', 'last_name', 'address', 'phone', 'balance'
        Supplier.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            balance=request.POST.get('balance')
        )
        return redirect('supplier_list_page')  # Redirect to the supplier list page

    # Render the form to add a new supplier
    return render(request, 'add_supplier.html')

# Function to remove a supplier
def remove_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    supplier.delete()
    return redirect('supplier_list_page')  # Redirect to the supplier list page

# Similar functions for adding/removing products, employees, etc.

# Function to add a new employee
def add_employee(request):
    if request.method == 'POST':
        # Handle the form data and save the new employee
        # Assuming you have a form with fields 'first_name', 'last_name', 'address', 'phone', 'daily_salary', 'centre'
        Employee.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            daily_salary=request.POST.get('daily_salary'),
            centre=request.POST.get('centre')
        )
        return redirect('employee_list_page')  # Redirect to the employee list page

    # Render the form to add a new employee
    return render(request, 'add_employee.html')

# Function to remove an employee
def remove_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return redirect('employee_list_page')  # Redirect to the employee list page

# Similarly, you can continue to implement functions for other operations and create corresponding HTML templates for the forms and list pages.

