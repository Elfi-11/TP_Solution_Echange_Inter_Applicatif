from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cats.views import CatMarkAdoptedView, CatViewSet, OwnerViewSet

router = DefaultRouter()
router.register(r"owners", OwnerViewSet, basename="owner")
router.register(r"cats", CatViewSet, basename="cat")

urlpatterns = [
    path("", include(router.urls)),
    path("cats/<int:pk>/adopter/", CatMarkAdoptedView.as_view(), name="cat-adopter"),
]
