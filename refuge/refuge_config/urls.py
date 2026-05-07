from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from refuge_app.views import home_refuge

urlpatterns = [
    path("", home_refuge, name="home"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("api/", include("refuge_app.urls")),
]
