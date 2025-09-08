import random
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import *
from django.utils.timezone import is_naive, make_naive
from .utils import get_currency_data, get_currency_data_test_error, get_currency_data_test_success, get_goods_data, get_goods_data_test_error, get_goods_data_test_success,post_goods_data_anae, post_currency_data_anae, post_goods_item_anae
from getpass import getpass
import requests
from decimal import Decimal, InvalidOperation
from django.conf import settings
from .models import PostCurrencyRequest
from rest_framework import status as http_status
from django.views.decorators.csrf import csrf_exempt
from .utils import RESULTS__C_SUCCESS_TEST, RESULTS__C_ERROR_TEST, RESULTS__G_SUCCESS_TEST, RESULTS__G_ERROR_TEST
from django.db.models import Q
from rest_framework import status
from django.db import transaction

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
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_api_goods(request):
    payload = request.data
    if not isinstance(payload, dict):
        return Response({"error": "Invalid JSON body."}, status=status.HTTP_400_BAD_REQUEST)

    pdls = payload.get("pdls") or {}
    if not isinstance(pdls, dict):
        return Response({"error": "'pdls' must be an object."}, status=status.HTTP_400_BAD_REQUEST)

    # ----- Declaration number (required) -----
    # accept either top-level "microImpDclrNo" or "declaration" (tolerant key)
    declaration_no = (payload.get("microImpDclrNo") or payload.get("declaration") or "").strip()
    if not declaration_no:
        return Response({"error": "microImpDclrNo is required at top-level."}, status=status.HTTP_400_BAD_REQUEST)


    # ----- Accept code from pdls or top-level -----
    code = (pdls.get("code") or payload.get("code") or "").strip()
    if not code:
        return Response({"error": "code is required in 'pdls.code' (or top-level)."}, status=status.HTTP_400_BAD_REQUEST)

    # ----- Extract pdls fields (tolerant keys) -----
    name = (pdls.get("pdlsNm") or pdls.get("name") or "").strip() or None
    qty = pdls.get("qty")
    qty_ut_cd = (pdls.get("qtyUtCd") or "").strip() or None
    currency = (pdls.get("frxcgCurrCd") or pdls.get("currency") or "").strip().upper() or None
    ut_decl_amt = pdls.get("utDclrAmt")     # unit value declared (foreign currency)
    unit_val_dzd = pdls.get("unitValDzd")   # optional
    line_val_dzd = pdls.get("lineValDzd")   # optional

    # ----- Casting helpers -----
    def to_decimal(v, field):
        if v is None:
            return None
        try:
            return Decimal(str(v))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError(f"'{field}' must be a number.")

    try:
        qty_int = int(qty) if qty is not None else None
    except (ValueError, TypeError):
        return Response({"error": "'qty' must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ut_decl_amt_dec = to_decimal(ut_decl_amt, "utDclrAmt") if ut_decl_amt is not None else None
        unit_val_dzd_dec = to_decimal(unit_val_dzd, "unitValDzd") if unit_val_dzd is not None else None
        line_val_dzd_dec = to_decimal(line_val_dzd, "lineValDzd") if line_val_dzd is not None else None
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ----- Required fields check -----
    missing = []
    if name is None: missing.append("pdlsNm")
    if qty_int is None: missing.append("qty")
    if qty_ut_cd is None: missing.append("qtyUtCd")
    if currency is None: missing.append("frxcgCurrCd")
    if ut_decl_amt_dec is None: missing.append("utDclrAmt")
    if missing:
        return Response({"error": "Missing required pdls fields.", "fields": missing}, status=status.HTTP_400_BAD_REQUEST)

    # ----- Back-calc per-unit DZD if only total and qty provided -----
    if unit_val_dzd_dec is None and line_val_dzd_dec is not None and qty_int:
        unit_val_dzd_dec = (line_val_dzd_dec / Decimal(qty_int)).quantize(Decimal("0.001"))

    # ----- Optional Unit resolution (if you have a Unit model) -----
    # unit = None
    # if qty_ut_cd:
    #     unit = Unit.objects.filter(
    #         Q(code__iexact=qty_ut_cd) | Q(abbr__iexact=qty_ut_cd) | Q(name__iexact=qty_ut_cd)
    #     ).first()
    #     if not unit:
    #         return Response({"error": "Unknown unit.", "qtyUtCd": qty_ut_cd}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        obj, created = GoodsItem.objects.select_for_update().get_or_create(
            code=code,
            defaults={
                "name": name,
                "quantity": qty_int,
                "unit": qty_ut_cd,           # or unit if using Unit FK
                "currency": currency,
                "unit_value_declared": ut_decl_amt_dec,
                # store declaration
                "declaration": declaration_no,    # if CharField, use: declaration_no
                **({"unit_value_dzd": unit_val_dzd_dec} if unit_val_dzd_dec is not None else {}),
                "json_after": payload,
            },
        )

        if not created:
            obj.name = name
            obj.quantity = qty_int
            obj.unit = qty_ut_cd             # or unit
            obj.currency = currency
            obj.unit_value_declared = ut_decl_amt_dec
            if unit_val_dzd_dec is not None:
                obj.unit_value_dzd = unit_val_dzd_dec
            obj.declaration = declaration_no   # if CharField: declaration_no
            obj.json_after = payload
            obj.save()

    # Post-hook (non-fatal)
    try:
        post_goods_item_anae(payload)
    except requests.RequestException:
        pass

    # Safe serialization helpers
    def iso(dt):
        if dt is None:
            return None
        # ensure naive in server tz or convert to ISO string
        return (make_naive(dt) if is_naive(dt) else dt).isoformat()

    response_data = {
        "message": "GoodsItem created successfully." if created else "GoodsItem updated successfully.",
        "created": created,
        "code": obj.code,
        "name": obj.name,
        "quantity": obj.quantity,
        "unit": getattr(obj.unit, "code", str(obj.unit)) if obj.unit else None,
        "currency": obj.currency,
        "unit_value_declared": str(obj.unit_value_declared) if obj.unit_value_declared is not None else None,
        "unit_value_dzd": str(obj.unit_value_dzd) if obj.unit_value_dzd is not None else None,
        "total_value_dzd": str(getattr(obj, "total_value_dzd", None)) if getattr(obj, "total_value_dzd", None) is not None else None,
        # return declaration number (handles FK or CharField)
        "declaration": getattr(obj.declaration, "number", obj.declaration) if getattr(obj, "declaration", None) else None,
        "updated_at": iso(getattr(obj, "updated_at", None)),
    }
    return Response(response_data, status=status.HTTP_200_OK)