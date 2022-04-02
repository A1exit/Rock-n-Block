from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tokens/', include('api.urls'))
]

schema_view = get_schema_view(
    openapi.Info(
        title="Rock-n-block API",
        default_version='v1',
        description="Документация для приложения api проекта Rock-n-block",
        contact=openapi.Contact(email="admin@kittygram.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
