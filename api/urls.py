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

    ### NESDA endpoints
    path("nesda/<str:table_key>/", nesda_collection),
    path("nesda/<str:table_key>/<int:row_id>/", nesda_item),
    path("nesda/by-date/", nesda_by_date_finance),

    ### NESDA endpoints
    path("angem/<str:table_key>/", angem_collection),
    path("angem/<str:table_key>/<int:row_id>/", angem_item),
    path("angem/<str:table_key>/by-date/", angem_by_date_finance),
]