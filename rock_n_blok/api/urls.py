from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ListTokensViewSet, create, total_supply

router = SimpleRouter()

router.register('list', ListTokensViewSet, basename='list')

urlpatterns = [
    path('create/', create),
    path('total_supply/', total_supply),
    path('', include(router.urls)),
]
