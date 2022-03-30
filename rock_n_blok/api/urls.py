from django.urls import path

from .views import create, list

urlpatterns = [
    path('create/', create),
    path('list/', list)
]
