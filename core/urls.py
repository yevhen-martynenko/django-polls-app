from django.urls import path

from .views import (
    main,
    remove, 
    create,
    vote,
    results,
    edit,
)


app_name = 'core'
urlpatterns = [
    path('', main, name='main'),
    path('create/', create, name='create'),
    path('delete/<str:code>/', remove, name='delete'),
    path('<str:code>/', vote, name='vote'),
    path('<str:code>/results/', results, name='results'),
    path('<str:code>/edit/', edit, name='edit'),
]
