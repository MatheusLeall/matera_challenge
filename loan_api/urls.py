from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Matera API",
        default_version="v1",
        description="Matera challenge loan API",
        terms_of_service="https://www.suaapi.com/terms/",
        contact=openapi.Contact(email="contato@suaapi.com"),
        license=openapi.License(name="Licença da sua API"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("loans.urls")),
    path("api/token/", obtain_auth_token, name="api_token_auth"),
    path(
        "api/v1/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/v1/redoc/", include_docs_urls(title="API Documentation", public=True)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]
