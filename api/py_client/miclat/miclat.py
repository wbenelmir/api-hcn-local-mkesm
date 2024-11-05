# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect
import requests

from getpass import getpass
# from django.conf import settings


def login():
    auth_endpoint = "http://172.16.18.52/api/Auth/login" 
    auth_response = requests.post(auth_endpoint, json={"user": "MDPMCME_ecapi2022","password": "Myeuy@@çèé&$$@@lKhv2033"}) 

    if auth_response.status_code == 200:
        token = auth_response.json()['token']
        key = 'Bearer'
        headers = {
            "Authorization": f"{key} {token}"
        }
        return headers
    return -1

def get_data(nin):
    headers = login()
    if headers != -1:
        endpoint = "http://172.16.18.52/api/MICLAT/GetIdentiteSecond?nin=" + nin
        get_response = requests.get(endpoint, headers=headers) 
        return get_response
    else:
        return -1

data = get_data('109980020000060005')
print(data.json())
