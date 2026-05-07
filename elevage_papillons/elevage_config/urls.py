from django.contrib import admin
from django.urls import include, path

from papillons.views import home_elevage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("papillons.urls")),
    path("", home_elevage, name="home"),
]