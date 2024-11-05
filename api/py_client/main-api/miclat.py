from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import requests

from getpass import getpass
from django.conf import settings


def login():
    auth_endpoint = "https://miclat.innovation-gov.dz/api/auth/" 
    auth_response = requests.post(auth_endpoint, json={"username": "mhNsg8qGZT93YL52pyJfaF","password": "F_GB5>$(]E&3e*f-Vp~wdP"}) 

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
        endpoint = "https://miclat.innovation-gov.dz/api/get/109920887131810000/"
        get_response = requests.get(endpoint, headers=headers) 
        return get_response
    else:
        return -1

data = get_data('109920887131810000')
print(data.json())
