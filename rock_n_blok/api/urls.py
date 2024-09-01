from django.urls import path

from .views import TokenListAPIView, create_token, get_total_supply

urlpatterns = [
    path("create/", create_token),
    path("total_supply/", get_total_supply),
    path("list/", TokenListAPIView.as_view()),
]
