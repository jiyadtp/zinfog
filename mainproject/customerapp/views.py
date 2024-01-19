import json

from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
import re
from django.contrib.auth import authenticate,login
from . models import *

# Create your views here.

def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('customer-product')
        else:
            messages.error(request, str("Invalid Credentials"))
            return redirect(request.META['HTTP_REFERER'])
    return render(request,"index.html")

def login_check_customer(request):
    email = request.GET.get("email")
    password = request.GET.get("password")
    required_fields = []
    if not email:
        required_fields.append("Email")
    if not password:
        required_fields.append("Password")
    if required_fields:
        response = f"{', '.join(required_fields)} are required"
        return JsonResponse({"message": response, "status": "error"})
    user = User.objects.filter(username=email).first()
    if not user:
        return JsonResponse({"message": "Invalid Datas", "status": "error"})
    elif not user.check_password(password):
        return JsonResponse({"message": "Invalid Password", "status": "error"})
    else:
        return JsonResponse({"message": "success", "status": "success"})

def sign_up(request):
    if request.method == "POST":
        messages.success(request, str("Successfully Registered"))
        return redirect("/")
    return render(request,"sign_up.html")

def register_data(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        phone = request.POST.get("phone").strip()
        required_fields = []
        if not name:
            required_fields.append("Name")
        if not email:
            required_fields.append("Email")
        if not password:
            required_fields.append("Password")
        if not phone:
            required_fields.append("Phone")
        if required_fields:
            response = f"{', '.join(required_fields)} are required"
            return JsonResponse({"message": response, "status": "error"})
        if User.objects.filter(username=email).exists():
            return JsonResponse({"message": "email exists", "status": "error"})
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JsonResponse({"message": "not a valid email", "status": "error"})
        user = User.objects.create_user(username=email, password=password)
        data_create = Customers.objects.create(
            auth_user=user,
            name=name,
            email=email,
            password=password,
            phone=phone
        )
        return JsonResponse({"message": "success", "status": "success"})

def customer_products(request):
    type_data = "products"
    data = Products.objects.all()
    customer = Customers.objects.get(auth_user=request.user)
    cart_count = Orders.objects.filter(customer_id=customer,status = "cart").count()
    context = {
        'type_data': type_data,
        'data':data,
        'cart_count':cart_count
    }
    return render(request,"customer/products.html",context)

def cart(request):
    if request.method == "POST":
        messages.success(request, str("Success"))
        return redirect("cart")
    type_data = "cart"
    customer = Customers.objects.get(auth_user=request.user)
    data = Orders.objects.filter(customer_id=customer,status = "cart")
    cart_count = Orders.objects.filter(customer_id=customer,status="cart").count()
    address_details = OrderAddress.objects.filter(customer_id=customer)
    context = {
        'type_data': type_data,
        'data': data,
        'cart_count': cart_count,
        'address_details':address_details,
    }
    return render(request, "customer/cart.html", context)

def add_to_cart(request):
    if request.method == "POST":
        messages.success(request, str("Added Successfully"))
        return redirect("customer-product")
    product_id = request.GET.get("productId")
    count = request.GET.get("count")
    customer = Customers.objects.get(auth_user=request.user)
    data_create = Orders.objects.create(
        customer_id_id = customer.id,
        product_id_id = product_id,
        status = "cart",
        total_count = count,
    )
    return JsonResponse({"message": "success", "status": "success"})

def buy_now(request):
    if request.method == "POST":
        customer = Customers.objects.get(auth_user=request.user)
        address = request.POST.get("address")
        required_fields = []
        if not address:
            required_fields.append("Address")
        if required_fields:
            response = f"{', '.join(required_fields)} is required"
            return JsonResponse({"message": response, "status": "error"})
        checkboxValues = json.loads(request.POST.get("checkboxValues"))
        for i in checkboxValues:
            data_order = Orders.objects.filter(id=i).update(
                order_status = "Pending",
                status = "Ordered",
                address = address
            )
        save_address = OrderAddress.objects.create(
            customer_id_id=customer.id,
            address=address
        )
        return JsonResponse({"message": "success", "status": "success"})

def delete_order(request,id):
    data_delete = Orders.objects.filter(id=id).delete()
    messages.success(request, str("Deleted"))
    return redirect(request.META['HTTP_REFERER'])


def customer_orders(request):
    type_data = "orders"
    customer = Customers.objects.get(auth_user=request.user)
    data = Orders.objects.filter(customer_id=customer, status="Ordered")
    cart_count = Orders.objects.filter(customer_id=customer, status="cart").count()
    context = {
        'type_data': type_data,
        'data': data,
        'cart_count': cart_count
    }
    return render(request, "customer/orders.html", context)


from django.db.models import Sum
def rate_products(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        total_rating = request.POST.get("total_rating")
        customer = Customers.objects.get(auth_user=request.user)
        order_check = ProductRating.objects.filter(customer_id=customer, product_id_id=product_id).first()
        if order_check:
            ProductRating.objects.filter(customer_id=customer, product_id_id=product_id).update(total_rating = total_rating)
        else:
            data_update = ProductRating.objects.create(
                customer_id = customer,
                product_id_id = product_id,
                total_rating = total_rating
            )
        total_count = ProductRating.objects.filter(product_id_id=product_id).aggregate(total_count=Sum('total_rating'))['total_count']
        count = ProductRating.objects.filter(product_id_id=product_id).count()
        avg = int(total_count/count)
        product_update = Products.objects.filter(id=product_id).update(avg_rating=int(avg))
        messages.success(request, str("Success"))
        return redirect('customer-orders')
    id = request.GET.get("id")
    data = Products.objects.get(id=id)
    customer = Customers.objects.get(auth_user=request.user)
    order_check = ProductRating.objects.filter(customer_id=customer,product_id_id=id).first()
    if order_check:
        rating = int(order_check.total_rating)
    else:
        rating = 0
    context = {
        'data': data,
        'rating':rating
    }
    return render(request, "customer/rate_products.html", context)


