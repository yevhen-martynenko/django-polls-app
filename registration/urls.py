from django.urls import path

from .views import (
    sign_in,
    sign_out,
    sign_up,
    activate,
    account,
    delete_account,
    reset_password,
    reset,
)


app_name = 'registration'
urlpatterns = [
    path('', sign_up, name='sign_up'),
    path('signin/', sign_in, name='sign_in'),
    path('signout/', sign_out, name='sign_out'),
    path('activate/<str:uidb64>/<str:code>/', activate, name='activate'),
    path('account/', account, name='account'),
    path('account/delete/', delete_account, name='delete_account'),
    path('reset_password/', reset_password, name='reset_password'),
    path('reset_password/<str:uidb64>/<str:code>/', reset, name='reset'),
]
