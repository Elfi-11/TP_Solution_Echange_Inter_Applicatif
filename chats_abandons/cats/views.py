from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from cats.models import Cat, Owner
from cats.serializers import CatSerializer, OwnerSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("id")
    serializer_class = OwnerSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.select_related("owner").all().order_by("id")
    serializer_class = CatSerializer


class CatMarkAdoptedView(APIView):
    def post(self, request, pk):
        cat = get_object_or_404(Cat.objects.select_related("owner"), pk=pk)
        cat.is_adopted = True
        cat.save(update_fields=["is_adopted"])
        return Response(CatSerializer(cat).data, status=status.HTTP_200_OK)


def home(request):
    owners = Owner.objects.prefetch_related("cats").all().order_by("id")
    cats = Cat.objects.select_related("owner").all().order_by("is_adopted", "id")

    return render(
        request,
        "cats/home.html",
        {
            "owners": owners,
            "cats": cats,
        },
    )
