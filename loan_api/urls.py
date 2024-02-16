from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("panel/", admin.site.urls),
    path("api/v1/", include("loans.urls")),
]
