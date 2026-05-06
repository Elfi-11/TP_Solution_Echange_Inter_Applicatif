from django.urls import path

from .views import AdopterPapillonView, AdoptionListView, ExternePapillonDisponibleListView

urlpatterns = [
    path("papillons/disponibles/", ExternePapillonDisponibleListView.as_view(), name="externe-disponibles"),
    path("adoptions/", AdoptionListView.as_view(), name="adoption-list"),
    path("adoptions/adopter/<int:papillon_id>/", AdopterPapillonView.as_view(), name="adopter-papillon"),
]
