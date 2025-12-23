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
from django.db import connection, transaction
# ---------- helpers ----------

def dictfetchall(cursor):
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    cols = [c[0] for c in cursor.description]
    return dict(zip(cols, row))

def q_ident(name: str) -> str:
    # Quote identifier for Postgres (still must whitelist!)
    return '"' + name.replace('"', '""') + '"'

# ---------- table configs (whitelists) ----------

TABLES = {
    "nesda": {
        "schema": "public",
        "db_table": "nesda",
        "pk": "id",
        "columns": {
            "PrenomAr_P", "NomAr_P", "birth_date", "Num_Act", "Code_Commune_Nais",
            "PrenomFr_P", "NomFr_P", "NIN", "date_finance", "type_finance",
            "NumNesda", "DDN_P",
        },
        "default_order_by": "id",
    },

    "angem": {
        "schema": "public",
        "db_table": "angem",
        "pk": "id",
        "columns": {
            "prenom_ar", "nom_ar", "acte", "code_commune",
            "prenom", "nom", "nin",
            "type_finance", "date_naissance", "date_financement",
        },
        "default_order_by": "id",
    },
}

def get_cfg(table_key: str):
    return TABLES.get(table_key)

def full_table_name(cfg) -> str:
    return f"{q_ident(cfg['schema'])}.{q_ident(cfg['db_table'])}"

def select_list(cfg) -> str:
    # If you want specific columns only, set cfg["select_columns"] = {...}
    cols = cfg.get("select_columns")
    if not cols:
        return "*"
    # whitelist enforcement:
    safe = [c for c in cols if c == cfg["pk"] or c in cfg["columns"]]
    return ", ".join(q_ident(c) for c in safe)

# ---------- endpoints ----------

TABLES = {
    "nesda": {
        "schema": "public",
        "db_table": "nesda",
        "pk": "id",
        "columns": {
            "PrenomAr_P",
            "NomAr_P",
            "birth_date",
            "Num_Act",
            "Code_Commune_Nais",
            "PrenomFr_P",
            "NomFr_P",
            "NIN",
            "date_finance",
            "type_finance",
            "NumNesda"
        },
        "default_order_by": "id",
        "max_limit": 500,
    },
    "angem": {
        "schema": "public",
        "db_table": "angem",  # Mixed case => must be quoted; q_ident handles it
        "pk": "id",
        "columns": {
            "prenom_ar",
            "nom_ar",
            "acte",
            "code_commune",
            "prenom",
            "nom",
            "nin",
            "type_finance",
            "date_naissance",
            "date_financement",
        },
        "default_order_by": "id",
        "max_limit": 500,
    }
}

def parse_dates(request):
    date_from = request.query_params.get("from")  # "YYYY-MM-DD"
    date_to = request.query_params.get("to")      # "YYYY-MM-DD"
    if not date_from or not date_to:
        return None, None, Response(
            {"error": "use query params ?from=YYYY-MM-DD&to=YYYY-MM-DD"},
            status=400
        )
    return date_from, date_to, None

@api_view(["GET"])
def nesda_by_date_finance(request, table_key: str):
    """
    GET /api/nesda/by-date/?from=2025-01-01&to=2025-12-31
    Filters by nesda.date_finance (date)
    """
    if table_key not in  {"angem"}:
        return Response({"error": "unknown table"}, status=400)
    
    cfg = get_cfg("nesda")
    date_from, date_to, err = parse_dates(request)
    if err:
        return err

    sql = f"""
        SELECT *
        FROM {full_table_name(cfg)}
        WHERE {q_ident("date_finance")} BETWEEN %s AND %s
        ORDER BY {q_ident("id")} DESC
        LIMIT 1000
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [date_from, date_to])
        rows = dictfetchall(cursor)

    return Response({"ok": True, "count": len(rows), "results": rows}, status=200)

def get_cfg(table_key: str):
    return TABLES.get(table_key)

@api_view(["GET", "POST"])
def nesda_collection(request, table_key: str):
    
    if table_key not in  {"nesda"}:
        return Response({"error": "unknown table"}, status=400)

    cfg = get_cfg(table_key)
    if not cfg:
        return Response({"error": "unknown table"}, status=400)

    if request.method == "GET":
        order_by = cfg.get("default_order_by", cfg["pk"])
        if order_by != cfg["pk"] and order_by not in cfg["columns"]:
            order_by = cfg["pk"]

        sql = f"""
            SELECT *
            FROM {full_table_name(cfg)}
            ORDER BY {q_ident(order_by)} DESC
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = dictfetchall(cursor)

        return Response(
            {"ok": True, "count": len(rows), "results": rows},
            status=200
        )

    # ---------- POST INSERT ----------
    payload = request.data or {}
    data = {k: payload[k] for k in payload.keys() if k in cfg["columns"]}

    if not data:
        return Response({"error": "no allowed fields provided"}, status=400)

    cols = list(data.keys())
    vals = [data[c] for c in cols]

    cols_sql = ", ".join(q_ident(c) for c in cols)
    placeholders = ", ".join(["%s"] * len(cols))

    sql = f"""
        INSERT INTO {full_table_name(cfg)} ({cols_sql})
        VALUES ({placeholders})
        RETURNING *
    """

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(sql, vals)
            row = dictfetchone(cursor)

    return Response({"ok": True, "row": row}, status=status.HTTP_201_CREATED)

@api_view(["GET", "PUT", "PATCH"])
def nesda_item(request, table_key: str, row_id: int):
    """
    GET   /api/<table_key>/<id>/  -> get one
    PATCH /api/<table_key>/<id>/  -> update one
    PUT   /api/<table_key>/<id>/  -> update one
    """
    if table_key not in  {"nesda"}:
        return Response({"error": "unknown table"}, status=400)

    cfg = get_cfg(table_key)
    if not cfg:
        return Response({"error": "unknown table"}, status=400)

    pk = cfg["pk"]

    if request.method == "GET":
        sql = f"""
            SELECT *
            FROM {full_table_name(cfg)}
            WHERE {q_ident(pk)} = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [row_id])
            row = dictfetchone(cursor)

        if row is None:
            return Response({"error": "not found"}, status=404)

        return Response({"ok": True, "row": row}, status=200)

    # UPDATE
    payload = request.data or {}
    data = {k: payload[k] for k in payload.keys() if k in cfg["columns"]}
    if not data:
        return Response({"error": "no allowed fields provided"}, status=400)

    set_sql = ", ".join(f"{q_ident(col)} = %s" for col in data.keys())
    vals = list(data.values()) + [row_id]

    sql = f"""
        UPDATE {full_table_name(cfg)}
        SET {set_sql}
        WHERE {q_ident(pk)} = %s
        RETURNING *
    """

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(sql, vals)
            row = dictfetchone(cursor)

    if row is None:
        return Response({"error": "not found"}, status=404)

    return Response({"ok": True, "row": row}, status=200)

@api_view(["GET", "POST"])
def angem_collection(request, table_key: str):
    
    if table_key not in  {"angem"}:
        return Response({"error": "unknown table"}, status=400)
    
    cfg = get_cfg(table_key)
    if not cfg:
        return Response({"error": "unknown table"}, status=400)

    if request.method == "GET":
        order_by = cfg.get("default_order_by", cfg["pk"])
        if order_by != cfg["pk"] and order_by not in cfg["columns"]:
            order_by = cfg["pk"]

        sql = f"""
            SELECT *
            FROM {full_table_name(cfg)}
            ORDER BY {q_ident(order_by)} DESC
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = dictfetchall(cursor)

        return Response({"ok": True, "count": len(rows), "results": rows}, status=200)

    # POST insert
    payload = request.data or {}
    data = {k: payload[k] for k in payload.keys() if k in cfg["columns"]}
    if not data:
        return Response({"error": "no allowed fields provided"}, status=400)

    cols = list(data.keys())
    vals = [data[c] for c in cols]

    cols_sql = ", ".join(q_ident(c) for c in cols)
    placeholders = ", ".join(["%s"] * len(cols))

    sql = f"""
        INSERT INTO {full_table_name(cfg)} ({cols_sql})
        VALUES ({placeholders})
        RETURNING *
    """

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(sql, vals)
            row = dictfetchone(cursor)

    return Response({"ok": True, "row": row}, status=status.HTTP_201_CREATED)

@api_view(["GET", "PATCH", "PUT"])
def angem_item(request, table_key: str, row_id: int):

    if table_key not in  {"angem"}:
        return Response({"error": "unknown table"}, status=400)
    
    cfg = get_cfg(table_key)
    if not cfg:
        return Response({"error": "unknown table"}, status=400)

    pk = cfg["pk"]

    if request.method == "GET":
        sql = f"""
            SELECT *
            FROM {full_table_name(cfg)}
            WHERE {q_ident(pk)} = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [row_id])
            row = dictfetchone(cursor)

        if row is None:
            return Response({"error": "not found"}, status=404)

        return Response({"ok": True, "row": row}, status=200)

    # UPDATE
    payload = request.data or {}
    data = {k: payload[k] for k in payload.keys() if k in cfg["columns"]}
    if not data:
        return Response({"error": "no allowed fields provided"}, status=400)

    set_sql = ", ".join(f"{q_ident(col)} = %s" for col in data.keys())
    vals = list(data.values()) + [row_id]

    sql = f"""
        UPDATE {full_table_name(cfg)}
        SET {set_sql}
        WHERE {q_ident(pk)} = %s
        RETURNING *
    """

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(sql, vals)
            row = dictfetchone(cursor)

    if row is None:
        return Response({"error": "not found"}, status=404)

    return Response({"ok": True, "row": row}, status=200)

@api_view(["GET"])
def angem_by_date_finance(request, table_key: str):
    """
    GET /api/angem/by-date/?from=2024-01-01&to=2024-12-31
    Filters by angem.date_financement (varchar -> date)
    """

    if table_key not in  {"angem"}:
        return Response({"error": "unknown table"}, status=400)

    cfg = get_cfg("angem")
    if not cfg:
        return Response({"error": "unknown table"}, status=400)

    date_from = request.query_params.get("from")
    date_to = request.query_params.get("to")

    if not date_from or not date_to:
        return Response(
            {"error": "use ?from=YYYY-MM-DD&to=YYYY-MM-DD"},
            status=400
        )

    sql = f"""
        SELECT *
        FROM {full_table_name(cfg)}
        WHERE NULLIF({q_ident("date_financement")}, '')::date
              BETWEEN %s AND %s
        ORDER BY {q_ident("id")} DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [date_from, date_to])
        rows = dictfetchall(cursor)

    return Response(
        {"ok": True, "count": len(rows), "results": rows},
        status=200
    )

# ---------------- Optional: convenience endpoints per table ----------------
# If you want fixed routes like /api/nesda/ without <table_key>, use these:

@api_view(["GET", "POST"])
def nesda(request):
    return nesda_collection(request, "nesda")

@api_view(["GET", "PUT", "PATCH"])
def nesda_one(request, row_id: int):
    return nesda_item(request, "nesda", row_id)

@api_view(["GET", "POST"])
def promoteurs(request):
    return nesda_collection(request, "promoteurs")

@api_view(["GET", "PUT", "PATCH"])
def promoteurs_one(request, row_id: int):
    return nesda_item(request, "promoteurs", row_id)