import requests
from django.conf import settings

RESULTS__C_SUCCESS_TEST = {
    "status": "Success",
    "message": "Déclaration reçue avec succès.",
    "declaration": {
        "microImpDclrNo": "MI-20250712-002",
        "microImpNo": "MS-20250712-001",
        "psnrFmnm": "MAMOUZI",
        "psnrGvnmNm": "Assia",
        "brdy": "19950526",
        "birtRegnNm": "Boumerdes",
        "gndrCd": "M",
        "psprNo": "123456789",
        "psprValdDt": "20300101",
        "psprNoIssDt": "20200101",
        "psprNoIssItt": "Boumerdes",
        "ntnalIdfyNo": "AB1234567",
        "natCd": "DZ",
        "dzaAddr": "Alger, Algérie",
        "tlphNo": "+213612345678",
        "eml": "assia.cntsid@gmail.com",
        "jobNm": "Ingénieur",
        "arvlDt": "20250715",
        "psnrBrlcCd": "FR",
        "psnrArlcCd": "DZ",
        "bggeTgcnt": "02",
        "bggeTamt": 38000.00,
        "pdlsList": [
            {
                "pdlsNm": "Montre de luxe",
                "qty": 1,
                "qtyUtCd": "NMB",
                "frxcgCurrCd": "EUR",
                "utDclrAmt": 19000.00,
                "relaNoSrno": "SN-XYZ-001",
                "microImpNo": "MS-20250712-001",
                "microImpDclrNo": "MI-20250712-002"
            },
            {
                "pdlsNm": "Montre de luxe",
                "qty": 1,
                "qtyUtCd": "NMB",
                "frxcgCurrCd": "EUR",
                "utDclrAmt": 19000.00,
                "relaNoSrno": "SN-XYZ-001",
                "microImpNo": "MS-20250712-001",
                "microImpDclrNo": "MI-20250712-002"
            }
        ]
    },
    "errors": []
}

RESULTS__C_ERROR_TEST = {
    "status": "Error",
    "message": "Votre déclaration comporte des erreurs.",
    "declaration": None,
    "errors": [
        {
            "code": "psprNoIssItt",
            "message": "Le lieu de délivrance du passeport est obligatoire",
            "declaration": None
        },
        {
            "code": "amtList[0].frxcgDzdAmt",
            "message": "Le montant en DZD est obligatoire",
            "declaration": None
        },
        {
            "code": "amtList[0].frxcgEurAmt",
            "message": "Le montant est obligatoire",
            "declaration": None
        },
        {
            "code": "brdy",
            "message": "La date de naissance est obligatoire",
            "declaration": None
        },
        {
            "code": "microImpNo",
            "message": "Le numéro de micro importateur est obligatoire",
            "declaration": None
        },
        {
            "code": "amtList[0].frxcgAmt",
            "message": "Le montant est obligatoire",
            "declaration": None
        },
        {
            "code": "amtList[0].frxcgCurrCd",
            "message": "Code de devise étrangère est obligatoire",
            "declaration": None
        },
        {
            "code": "gndrCd",
            "message": "Le code de sexe est obligatoire",
            "declaration": None
        },
        {
            "code": "birtRegnNm",
            "message": "Le lieu de naissance est obligatoire",
            "declaration": None
        },
        {
            "code": "psnrFmnm",
            "message": "Le nom du voyageur est obligatoire",
            "declaration": None
        },
        {
            "code": "microImpDclrNo",
            "message": "Le numéro de la déclaration est obligatoire",
            "declaration": None
        },
        {
            "code": "psprNoIssDt",
            "message": "La date de délivrance du passeport est obligatoire",
            "declaration": None
        },
        {
            "code": "psprValdDt",
            "message": "La date de validité du passeport est obligatoire",
            "declaration": None
        },
        {
            "code": "psprNo",
            "message": "Le numéro de passeport est obligatoire",
            "declaration": None
        },
        {
            "code": "natCd",
            "message": "Le code de nationalité est obligatoire",
            "declaration": None
        },
        {
            "code": "ntnalIdfyNo",
            "message": "Le NIN est obligatoire",
            "declaration": None
        },
        {
            "code": "psnrGvnmNm",
            "message": "Le prénom du voyageur est obligatoire",
            "declaration": None
        }
    ]
}

RESULTS__G_SUCCESS_TEST = {
    "status": "Success",
    "message": "Déclaration reçue avec succès.",
    "declaration": {
        "microImpDclrNo": "MI-20250712-002",
        "microImpNo": "MS-20250712-001",
        "psnrFmnm": "MAMOUZI",
        "psnrGvnmNm": "Assia",
        "brdy": "19950526",
        "birtRegnNm": "Boumerdes",
        "gndrCd": "M",
        "psprNo": "123456789",
        "psprValdDt": "20300101",
        "psprNoIssDt": "20200101",
        "psprNoIssItt": "Boumerdes",
        "ntnalIdfyNo": "AB1234567",
        "natCd": "DZ",
        "dzaAddr": "Alger, Algérie",
        "tlphNo": "+213612345678",
        "eml": "assia.cntsid@gmail.com",
        "jobNm": "Ingénieur",
        "arvlDt": "20250715",
        "psnrBrlcCd": "FR",
        "psnrArlcCd": "DZ",
        "bggeTgcnt": "02",
        "bggeTamt": 38000.00,
        "pdlsList": [
            {
                "pdlsNm": "Montre de luxe",
                "qty": 1,
                "qtyUtCd": "NMB",
                "frxcgCurrCd": "EUR",
                "utDclrAmt": 19000.00,
                "relaNoSrno": "SN-XYZ-001",
                "microImpNo": "MS-20250712-001",
                "microImpDclrNo": "MI-20250712-002"
            },
            {
                "pdlsNm": "Montre de luxe",
                "qty": 1,
                "qtyUtCd": "NMB",
                "frxcgCurrCd": "EUR",
                "utDclrAmt": 19000.00,
                "relaNoSrno": "SN-XYZ-001",
                "microImpNo": "MS-20250712-001",
                "microImpDclrNo": "MI-20250712-002"
            }
        ]
    },
    "errors": []
}

RESULTS__G_ERROR_TEST = {
    "status": "Error",
    "message": "Votre déclaration comporte des erreurs.",
    "declaration": None,
    "errors": [
        {
            "code": "pdlsList[1].utDclrAmt",
            "message": "La valeur unitaire déclarée est obligatoire",
            "declaration": None
        },
        {
            "code": "psnrGvnmNm",
            "message": "Le prénom du voyageur est obligatoire",
            "declaration": None
        },
        {
            "code": "brdy",
            "message": "La date de naissance est obligatoire",
            "declaration": None
        },
        {
            "code": "psprNo",
            "message": "Le numéro de passeport est obligatoire",
            "declaration": None
        },
        {
            "code": "pdlsList[1].pdlsNm",
            "message": "La description de l'article est obligatoire",
            "declaration": None
        },
        {
            "code": "gndrCd",
            "message": "Le code de sexe est obligatoire",
            "declaration": None
        },
        {
            "code": "pdlsList[1].qty",
            "message": "La quantité est obligatoire",
            "declaration": None
        },
        {
            "code": "microImpNo",
            "message": "Le numéro de micro importateur est obligatoire",
            "declaration": None
        },
        {
            "code": "psnrFmnm",
            "message": "Le nom du voyageur est obligatoire",
            "declaration": None
        },
        {
            "code": "microImpDclrNo",
            "message": "Le numéro de la déclaration est obligatoire",
            "declaration": None
        },
        {
            "code": "ntnalIdfyNo",
            "message": "Le NIN est obligatoire",
            "declaration": None
        },
        {
            "code": "birtRegnNm",
            "message": "Le lieu de naissance est obligatoire",
            "declaration": None
        },
        {
            "code": "psprNoIssDt",
            "message": "La date de délivrance du passeport est obligatoire",
            "declaration": None
        },
        {
            "code": "natCd",
            "message": "Le code de nationalité est obligatoire",
            "declaration": None
        },
        {
            "code": "pdlsList[1].qtyUtCd",
            "message": "Le code d'unité de quantité est obligatoire",
            "declaration": None
        },
        {
            "code": "pdlsList[1].frxcgCurrCd",
            "message": "Le code de devise étrangère est obligatoire",
            "declaration": None
        },
        {
            "code": "psprValdDt",
            "message": "La date de validité du passeport est obligatoire",
            "declaration": None
        },
        {
            "code": "psprNoIssItt",
            "message": "Le lieu de délivrance du passeport est obligatoire",
            "declaration": None
        }
    ]
}

def douanes_test_login():
    response = requests.post(
        settings.DOUANES_LOGIN_DOUANES_TEST ,
        json={"username": settings.DOUANES_USER_TEST , "password": settings.DOUANES_PASSWORD_TEST }
    )
    print(f"response-login : {response}")
    if response.status_code == 200:
        token = response.json().get('token')
        return {"Authorization": f"Bearer {token}"}
    return None

def douanes_login():
    response = requests.post(
        settings.DOUANES_LOGIN_DOUANES,
        json={"username": settings.DOUANES_USER, "password": settings.DOUANES_PASSWORD}
    )
    print(f"response-login : {response}")
    if response.status_code == 200:
        token = response.json().get('token')
        return {"Authorization": f"Bearer {token}"}
    return None

def anae_login():
    response = requests.post(
        settings.ANAE_LOGIN_DOUANES,
        json={"username": settings.ANAE_DOUANES_USER, "password": settings.ANAE_DOUANES_PASSWORD}
    )
    print(f"response-login : {response}")
    if response.status_code == 200:
        token = response.json().get('token')
        return {"Authorization": f"Bearer {token}"}
    return None

def get_currency_data_test_success(json_data):
    headers = douanes_test_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.DOUANES_POST_DATA_CURRENCY_TEST_SUCCESS
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None

def get_currency_data_test_error(json_data):
    headers = douanes_test_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.DOUANES_POST_DATA_CURRENCY_TEST_ERROR
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None

def get_currency_data(json_data):
    headers = douanes_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.DOUANES_POST_DATA_CURRENCY
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None

def get_goods_data_test_success(json_data):
    headers = douanes_test_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.DOUANES_POST_DATA_GOODS_TEST_SUCCESS
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None

def get_goods_data_test_error(json_data):
    headers = douanes_test_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.DOUANES_POST_DATA_GOODS_TEST_ERROR
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None

def get_goods_data(json_data):
    headers = douanes_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.DOUANES_POST_DATA_GOODS
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None

def post_goods_data_anae(json_data):
    headers = anae_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.LOCAL_API_DOUANES_PUT_DATA_GOODS
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None

def post_currency_data_anae(json_data):
    headers = anae_login()
    print(f"headers : {headers}")
    if not headers:
        return None

    endpoint = settings.LOCAL_API_DOUANES_PUT_DATA_CURRENCY
    response = requests.post(endpoint, headers=headers, json=json_data)
    print(f"response: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    return None
