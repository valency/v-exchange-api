from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from vex_auth.views import check_admin
from vex_exchange.serializers import *


@api_view(["GET", "POST"])
def stock(request):
    if check_admin(request) is not None:
        if request.method == "GET":
            if "id" in request.GET:
                try:
                    return Response(StockSerializer(Stock.objects.get(id=request.GET["id"])).data)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "POST":
            if "id" in request.data and "name" in request.data:
                s = Stock(id=request.data["id"], name=request.data["name"])
                s.save()
                return Response(StockSerializer(s).data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
