from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnimalViewSet, EspeceViewSet

router = DefaultRouter()
router.register(r"especes", EspeceViewSet, basename="espece")
router.register(r"animaux", AnimalViewSet, basename="animal")

urlpatterns = [
    path("", include(router.urls)),
]