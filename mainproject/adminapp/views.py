from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
import re
from customerapp.models import Customers,Products,Orders

# Create your views here.

def admin_login(request):
    if request.method == "POST":
        return redirect('dashboard')
    return render(request,"admin_login.html")

def login_check(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    required_fields = []
    if not username:
        required_fields.append("Username")
    if not password:
        required_fields.append("Password")
    if required_fields:
        response = f"{', '.join(required_fields)} are required"
        return JsonResponse({"message": response, "status": "error"})
    user = User.objects.filter(username=username).first()
    if not user:
        return JsonResponse({"message": "Invalid Datas", "status": "error"})
    elif not user.check_password(password):
        return JsonResponse({"message": "Invalid Password", "status": "error"})
    else:
        return JsonResponse({"message": "success", "status": "success"})

def dashboard(request):
    type_data = "dashboard"
    customer_count = Customers.objects.all().count()
    product_count = Products.objects.all().count()
    order_count = Orders.objects.filter(status="Ordered").count()
    context = {
        'type_data':type_data,
        'customer_count':customer_count,
        'product_count':product_count,
        'order_count':order_count
    }
    return render(request,"dashboard.html",context)

def customers(request):
    type_data = "customers"
    data = Customers.objects.all()
    context = {
        'type_data': type_data,
        'data':data
    }
    return render(request,"customers.html",context)

def products(request):
    if request.method == "POST":
        messages.success(request, str("Success"))
        return redirect(request.META['HTTP_REFERER'])
    type_data = "products"
    data = Products.objects.all()
    context = {
        'type_data': type_data,
        'data':data
    }
    return render(request,"products.html",context)

def create_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name").strip()
        required_fields = []
        if not product_name:
            required_fields.append("Product Name")
        if required_fields:
            response = f"{', '.join(required_fields)} is required"
            return JsonResponse({"message": response, "status": "error"})
        try:
            product_image = request.FILES['product_image']
        except:
            product_image = ""
        data_create = Products.objects.create(
            name=product_name,
            product_image=product_image,
        )
        return JsonResponse({"message": "success", "status": "success"})


def edit_product(request):
    id = request.GET.get("id")
    data = Products.objects.get(id=id)
    context = {
        'data':data
    }
    return render(request,"edit_product.html",context)

def edit_product_action(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_name = request.POST.get("product_name").strip()
        image_change = request.POST.get("image_change")
        required_fields = []
        if not product_name:
            required_fields.append("Product Name")
        if required_fields:
            response = f"{', '.join(required_fields)} is required"
            return JsonResponse({"message": response, "status": "error"})
        try:
            product_image = request.FILES['product_image']
        except:
            product_image = ""
        data_update = Products.objects.filter(id=product_id).update(
            name=product_name,
        )
        if image_change != "" or image_change != "no":
            data_save = Products.objects.get(id=product_id)
            data_save.product_image = product_image
            data_save.save()
        return JsonResponse({"message": "success", "status": "success"})

def delete_product(request,id):
    data_delete = Products.objects.filter(id=id).delete()
    messages.success(request, str("Deleted"))
    return redirect(request.META['HTTP_REFERER'])

def orders(request):
    type_data = "orders"
    data = Orders.objects.filter(status="Ordered")
    context = {
        'type_data': type_data,
        'data':data
    }
    return render(request,"orders.html",context)


def change_status(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        status_value = request.POST.get("status_value")
        data_update = Orders.objects.filter(id=order_id).update(order_status=status_value)
        messages.success(request, str("Changed Successfully"))
        return redirect('orders')
    id = request.GET.get("id")
    data = Orders.objects.get(id=id)
    context = {
        'data':data
    }
    return render(request,"change_status.html",context)