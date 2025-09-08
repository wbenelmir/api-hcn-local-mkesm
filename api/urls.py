from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import *

# /api/
urlpatterns = [
    path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    ### TESTS
    path('currency/test-success/', test_success_currency, name='test-success-currency'),
    path('currency/test-error/', test_error_currency, name='test-error-currency'),
    path('post-currency-request/error/', post_currency_error_request_view, name='post-error-currency-request'),
    path('post-currency-request/success/', post_currency_success_request_view, name='post-success-currency-request'),
    path('goods/test-success/', test_success_goods, name='test-success-goods'),
    path('goods/test-error/', test_error_goods, name='test-error-goods'),
    path('post-goods-request/error/', post_goods_error_request_view, name='post-error-goods-request'),
    path('post-goods-request/success/', post_goods_success_request_view, name='post-success-goods-request'),

    path('post-currency-request/', post_currency_request_view, name='post-currency-request'),
    path('post-goods-request/', post_goods_request_view, name='post-goods-request'),

    path('update-currency/', update_api_currency, name='update_api_currency'),
    path('update-marchandise/', update_api_marchandise, name='update_api_marchandise'),
    path('update-goods-item/', update_api_goods, name='import-update-api-goods'),
]