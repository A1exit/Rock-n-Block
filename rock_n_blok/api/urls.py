from django.urls import path

from .views import create, list, total_supply

urlpatterns = [
    path('create/', create),
    path('list/', list),
    path('total_supply/', total_supply)
]
