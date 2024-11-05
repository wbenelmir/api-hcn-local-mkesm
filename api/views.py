import random
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from getpass import getpass
import requests
from django.conf import settings
from .models import GetRequest

def login():
    auth_endpoint = settings.MICLAT_LOGIN_EP
    auth_response = requests.post(auth_endpoint, json={"user": settings.MICLAT_USER,"password": settings.MICLAT_PASSWORD}) 

    if auth_response.status_code == 200:
        token = auth_response.json()['token']
        key = 'Bearer'
        headers = {
            "Authorization": f"{key} {token}"
        }
        return headers
    return -1


# def login():
#     auth_endpoint = settings.MICLAT_LOGIN_EP
    
#     try:
#         user = settings.MICLAT_USER
#         password = settings.MICLAT_PASSWORD
#         auth_response = requests.post(auth_endpoint, json={"user": user,"password": password}) 

#         if auth_response.status_code == 200:
#             token = auth_response.json()['token']
#             key = 'Bearer'
#             headers = {
#                 "Authorization": f"{key} {token}"
#             }
#             return headers
#         else:
#             print(f"Authentication failed (MICLAT). Status code: {auth_response.status_code}")
#             print(auth_response.json())
#             return -1
#     except BaseException as e:
#         print(str(e))
#         return -1


def get_data(nin):
    print('login start')
    headers = login()
    print('login end')
    if headers != -1:
        endpoint = settings.MICLAT_GET_DATA + nin
        print('endpoint : ',endpoint)
        get_response = requests.get(endpoint, headers=headers) 
        print('get_response')
        return get_response
    else:
        return -1

    return data
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def calculate(request, operation):
    try:
        num1 = float(request.GET.get('x', 0))
        num2 = float(request.GET.get('y', 0))

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return Response({'error': 'Cannot divide by zero'}, status=400)
            result = num1 / num2
        else:
            return Response({'error': 'Invalid operation'}, status=400)

        return Response({'result': result})

    except ValueError:
        return Response({'error': 'Invalid input, please provide valid numbers'}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def miclat(request, nin):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(8))
    getreq = GetRequest.objects.create(
                code=randomstr,
                nin=nin,
                user = request.user,
            ) 
    try:
        result = get_data(nin)
        if result != -1:
            getreq.status = '200' 
            getreq.save()    
            print(result.json())
            return Response(result.json(), status=200)
        else:
            getreq.status = '500'  
            getreq.save() 
            return Response({'error': 'Invalid NIN, please provide valid value'}, status=500)
         
    except ValueError:
        getreq.status = '400'  
        getreq.save()  
        return Response({'error': '400'}, status=400)
    