import random
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import PostCurrencyRequest, PostMarchandiseRequest
from .utils import get_currency_data, get_currency_data_test_error, get_currency_data_test_success, get_goods_data, get_goods_data_test_error, get_goods_data_test_success,post_goods_data_anae, post_currency_data_anae
from getpass import getpass
import requests
from django.conf import settings
from .models import PostCurrencyRequest
from rest_framework import status as http_status
from django.views.decorators.csrf import csrf_exempt
from .utils import RESULTS__C_SUCCESS_TEST, RESULTS__C_ERROR_TEST, RESULTS__G_SUCCESS_TEST, RESULTS__G_ERROR_TEST
from django.db.models import Q
from rest_framework import status

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_currency_request_view(request):
    try:
        json_data = request.data
        code_request = request.data.get('microImpDclrNo', '/')

        post_instance = PostCurrencyRequest.objects.filter(
            code=code_request
        ).first()

        if post_instance:
            post_instance.user = request.user
            post_instance.post_data=json_data
            post_instance.code_request = code_request
            post_instance.save()
        else:
            post_instance = PostCurrencyRequest.objects.create(
                user=request.user,
                post_data=json_data,
                code_request = code_request,
                code = code_request,
                status="pending"
            )

        response_data = get_currency_data(json_data)

        if response_data and isinstance(response_data, dict):
            # result = response_data.get("result", {})
            rstatus = response_data.get("status", "inconnu")
            message = response_data.get("message", "")
            errors = response_data.get("errors", [])

            post_instance.return_data = response_data
            post_instance.status = "200"
            post_instance.rstatus = rstatus
            post_instance.message = message
            post_instance.errors = errors 
            post_instance.save()

            return Response(response_data, status=200)
        else:
            post_instance.status = "500"
            post_instance.save()
            return Response(
                {'error': 'Erreur de connexion à l’API douanière.'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        post_instance.status = "400"
        post_instance.save()
        return Response(
            {'error': str(e)},
            status=http_status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_currency_success_request_view(request):
    try:
        json_data = request.data
        code_request = request.data.get('microImpDclrNo', '/')

        post_instance = PostCurrencyRequest.objects.filter(
            code_request=code_request
        ).first()

        if post_instance:
            post_instance.user = request.user
            post_instance.post_data=json_data
            post_instance.code_request = code_request
            post_instance.save()
        else:
            post_instance = PostCurrencyRequest.objects.create(
                user=request.user,
                post_data=json_data,
                code_request = code_request,
                code = code_request,
                status="pending"
            )

        response_data = get_currency_data_test_success(json_data)

        if response_data and isinstance(response_data, dict):
            result = response_data.get("result", {})
            rstatus = result.get("status", "inconnu")
            message = result.get("message", "")
            errors = result.get("errors", [])

            post_instance.return_data = response_data
            post_instance.status = "200"
            post_instance.rstatus = rstatus
            post_instance.message = message
            post_instance.errors = errors 
            post_instance.save()

            return Response(response_data, status=200)
        else:
            post_instance.status = "500"
            post_instance.save()
            return Response(
                {'error': 'Erreur de connexion à l’API douanière.'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        post_instance.status = "400"
        post_instance.save()
        return Response(
            {'error': str(e)},
            status=http_status.HTTP_400_BAD_REQUEST
        )
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_currency_error_request_view(request):
    try:
        json_data = request.data
        code_request = request.data.get('microImpDclrNo', '/')

        post_instance = PostCurrencyRequest.objects.filter(
            code_request=code_request
        ).first()

        if post_instance:
            post_instance.user = request.user
            post_instance.post_data=json_data
            post_instance.code_request = code_request
            post_instance.save()
        else:
            post_instance = PostCurrencyRequest.objects.create(
                user=request.user,
                post_data=json_data,
                code_request = code_request,
                code = code_request,
                status="pending"
            )

        response_data = get_currency_data_test_error(json_data)

        if response_data and isinstance(response_data, dict):
            result = response_data.get("result", {})
            rstatus = result.get("status", "inconnu")
            message = result.get("message", "")
            errors = result.get("errors", [])

            post_instance.return_data = response_data
            post_instance.status = "200"
            post_instance.rstatus = rstatus
            post_instance.message = message
            post_instance.errors = errors 
            post_instance.save()

            return Response(response_data, status=200)
        else:
            post_instance.status = "500"
            post_instance.save()
            return Response(
                {'error': 'Erreur de connexion à l’API douanière.'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        post_instance.status = "400"
        post_instance.save()
        return Response(
            {'error': str(e)},
            status=http_status.HTTP_400_BAD_REQUEST
        )
    
@csrf_exempt
@api_view(['POST']) 
@permission_classes([IsAuthenticated, IsAdminUser])
def test_success_currency(request):
    result = {}
    try:
        result = RESULTS__C_SUCCESS_TEST
        return Response({'result': result})
    except ValueError:
        return Response({'error': 'error'}, status=400)
    
@csrf_exempt
@api_view(['POST']) 
@permission_classes([IsAuthenticated, IsAdminUser])
def test_error_currency(request):
    result = {}
    try:
        result = RESULTS__C_ERROR_TEST
        return Response({'result': result})
    except ValueError:
        return Response({'error': 'error'}, status=400)
     
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_goods_request_view(request):
    try:
        json_data = request.data
        code_request = request.data.get('microImpDclrNo', '/')

        post_instance = PostMarchandiseRequest.objects.filter(
            code_request=code_request
        ).first()

        if post_instance:
            post_instance.user = request.user
            post_instance.post_data=json_data
            post_instance.code_request = code_request
            post_instance.save()
        else:
            post_instance = PostMarchandiseRequest.objects.create(
                user=request.user,
                post_data=json_data,
                code_request = code_request,
                code = code_request,
                status="pending"
            )

        response_data = get_goods_data(json_data)

        if response_data and isinstance(response_data, dict):
            # result = response_data.get("result", {})
            rstatus = response_data.get("status", "inconnu")
            message = response_data.get("message", "")
            errors = response_data.get("errors", [])

            post_instance.return_data = response_data
            post_instance.status = "200"
            post_instance.rstatus = rstatus
            post_instance.message = message
            post_instance.errors = errors 
            post_instance.save()

            return Response(response_data, status=200)
        else:
            post_instance.status = "500"
            post_instance.save()
            return Response(
                {'error': 'Erreur de connexion à l’API douanière.'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        post_instance.status = "400"
        post_instance.save()
        return Response(
            {'error': str(e)},
            status=http_status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_goods_success_request_view(request):
    try:
        json_data = request.data
        code_request = request.data.get('microImpDclrNo', '/')

        post_instance = PostMarchandiseRequest.objects.filter(
            code_request=code_request
        ).first()

        if post_instance:
            post_instance.user = request.user
            post_instance.post_data=json_data
            post_instance.code_request = code_request
            post_instance.save()
        else:
            post_instance = PostMarchandiseRequest.objects.create(
                user=request.user,
                post_data=json_data,
                code_request = code_request,
                code = code_request,
                status="pending"
            )

        response_data = get_goods_data_test_success(json_data)

        if response_data and isinstance(response_data, dict):
            result = response_data.get("result", {})
            rstatus = result.get("status", "inconnu")
            message = result.get("message", "")
            errors = result.get("errors", [])

            post_instance.return_data = response_data
            post_instance.status = "200"
            post_instance.rstatus = rstatus
            post_instance.message = message
            post_instance.errors = errors 
            post_instance.save()

            return Response(response_data, status=200)
        else:
            post_instance.status = "500"
            post_instance.save()
            return Response(
                {'error': 'Erreur de connexion à l’API douanière.'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        post_instance.status = "400"
        post_instance.save()
        return Response(
            {'error': str(e)},
            status=http_status.HTTP_400_BAD_REQUEST
        )
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_goods_error_request_view(request):
    try:
        json_data = request.data
        code_request = request.data.get('microImpDclrNo', '/')

        post_instance = PostMarchandiseRequest.objects.filter(
            code_request=code_request
        ).first()

        if post_instance:
            post_instance.user = request.user
            post_instance.post_data=json_data
            post_instance.code_request = code_request
            post_instance.save()
        else:
            post_instance = PostMarchandiseRequest.objects.create(
                user=request.user,
                post_data=json_data,
                code_request = code_request,
                code = code_request,
                status="pending"
            )

        response_data = get_goods_data_test_error(json_data)

        if response_data and isinstance(response_data, dict):
            result = response_data.get("result", {})
            rstatus = result.get("status", "inconnu")
            message = result.get("message", "")
            errors = result.get("errors", [])

            post_instance.return_data = response_data
            post_instance.status = "200"
            post_instance.rstatus = rstatus
            post_instance.message = message
            post_instance.errors = errors 
            post_instance.save()

            return Response(response_data, status=200)
        else:
            post_instance.status = "500"
            post_instance.save()
            return Response(
                {'error': 'Erreur de connexion à l’API douanière.'},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        post_instance.status = "400"
        post_instance.save()
        return Response(
            {'error': str(e)},
            status=http_status.HTTP_400_BAD_REQUEST
        )
    
@csrf_exempt
@api_view(['POST']) 
@permission_classes([IsAuthenticated, IsAdminUser])
def test_success_goods(request):
    result = {}
    try:
        result = RESULTS__G_SUCCESS_TEST
        return Response({'result': result})
    except ValueError:
        return Response({'error': 'error'}, status=400)
    
@csrf_exempt
@api_view(['POST']) 
@permission_classes([IsAuthenticated, IsAdminUser])
def test_error_goods(request):
    result = {}
    try:
        result = RESULTS__G_ERROR_TEST
        return Response({'result': result})
    except ValueError:
        return Response({'error': 'error'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_api_currency(request):
    code = request.data.get('declaration_code')
    new_api_update = request.data
    update_api_anae = {}
    update_api_anae['api_update'] = new_api_update
    if not code or not new_api_update:
        return Response({"error": "declaration_code is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        obj = PostCurrencyRequest.objects.get(code=code)
        obj.api_update = new_api_update
        obj.save()

        try:
            update_api_anae['code'] = code
            post_currency_data_anae(update_api_anae)
        except requests.RequestException as e:
            pass
        
        return Response({"message": "PostCurrencyRequest updated successfully.", "code": obj.code}, status=200)
    except PostCurrencyRequest.DoesNotExist:
        return Response({"error": "No PostCurrencyRequest found with this code."}, status=404)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_api_marchandise(request):
    code = request.data.get('declaration_code')
    print(f"code : {code}")
    new_api_update = request.data
    update_api_anae = {}
    update_api_anae['api_update'] = new_api_update
    if not code or not new_api_update:
        return Response({"error": "declaration_code is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        obj = PostMarchandiseRequest.objects.get(code=code)
        obj.api_update = new_api_update
        obj.save()
        try:
            update_api_anae['code'] = code
            post_goods_data_anae(update_api_anae)
        except requests.RequestException as e:
            pass
        return Response({"message": "PostMarchandiseRequest updated successfully.", "code": obj.code}, status=200)
    except PostMarchandiseRequest.DoesNotExist:
        return Response({"error": "No PostMarchandiseRequest found with this code."}, status=404)
    
