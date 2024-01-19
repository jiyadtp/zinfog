from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
import re
from customerapp.models import Customers,Products,Orders
from . serializers import ProductSerializer,OrderDetails
from . authentication import create_access_token,decode_access_token
from rest_framework.authentication import get_authorization_header
from rest_framework import status

# Create your views here.


class SignUpApiview(APIView):
    def post(self,request):
        data = request.data

        if data['customer_name'].isspace() or data['customer_name'] == "":
            return JsonResponse({"message": "customer name is Manadatory", "status": False})
        if data['email'].isspace() or data['email'] == "":
            return JsonResponse({"message": "Email is Manadatory", "status": False})
        if data['phone'].isspace() or data['phone'] == "":
            return JsonResponse({"message": "phone is Manadatory", "status": False})
        if data['password'].isspace() or data['password'] == "":
            return JsonResponse({"message": "password is Manadatory", "status": False})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return Response({'message': "Enter Valid Email", "status": False})
        # if not re.search('[a-zA-Z]', data['password']) or not re.search('[0-9]', data['password']) or not re.search(
        #         '[!@#$%^&*(),.?":{}|<>]', data['password']) or len(data['password']) < 8:
        #     return JsonResponse({"message": "Password does not match the format", "status": False})
        elif User.objects.filter(username=data['email']).exists():
            return Response({'message':"An account with the given email-id already exists","status":False})
        else:
            user = User.objects.create_user(username = data['email'],password = data['password'])
            user.save()
            data_create = Customers.objects.create(
                auth_user=user,
                name=data['customer_name'],
                email=data['email'],
                password=data['password'],
                phone=data['phone']
            )

            return Response({'message':"sucessfully created","status":True})


class LoginApiview(APIView):
    def post(self,request):
        data = request.data
        user = User.objects.filter(username=data['username']).first()
        if not user:
            # raise APIException("Invalid credentials!")
            return Response({"message":"Invalid credentials",'status':False})

        if not user.check_password(data['password']):
            return Response({"message": "Invalid Password", 'status': False})

        encryption_key = 'customerkey'
        access_token = create_access_token(user.id,encryption_key)
        response = Response()
        response.data = {
            'token': access_token,
            'status':True,
            'username':user.username,
        }

        return response



class ProductListApiview(APIView):
    def get(self, request):
        queryset = Products.objects.all()
        serializer_class = ProductSerializer
        data_json = {}
        serializer = serializer_class(queryset, many=True)  # Instantiate the serializer
        data_json['product_list'] = serializer.data  # Serialize the data
        return Response(data_json)

product_listview = ProductListApiview.as_view()


from rest_framework.decorators import api_view
@api_view(['GET'])
def get_order_details(request):
    auth = get_authorization_header(request).split()
    if auth and len(auth) == 2:
        token = auth[1].decode('utf-8')
        encryption_key = 'customerkey'
        decoded = decode_access_token(token, encryption_key)
        if decoded is None or decoded == "":
            return Response({"message": "authorization error", 'status': False})
        user_id = decoded['user_id']
        user = User.objects.get(id=user_id)
        customer = Customers.objects.get(auth_user=user)
        queries = Orders.objects.filter(customer_id=customer, status="Ordered")
        serializer = OrderDetails(queries, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "Unauthorized", 'status': False})