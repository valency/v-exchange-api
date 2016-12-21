import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from vex.common import *
from vex_auth.serializers import *


def check_user(request):
    if "HTTP_VEX_USERNAME" in request.META and "HTTP_VEX_TICKET" in request.META:
        username = request.META.get("HTTP_VEX_USERNAME")
        ticket = request.META.get("HTTP_VEX_TICKET")
    elif "vex_username" in request.COOKIES and "vex_ticket" in request.COOKIES:
        username = request.COOKIES.get("vex_username")
        ticket = request.COOKIES.get("vex_ticket")
    else:
        return None
    try:
        user = Account.objects.get(username=username, ticket=ticket)
        return user
    except ObjectDoesNotExist:
        return None


def check_admin(request):
    user = check_user(request)
    if user.group == tuple_search(USER_GROUP, 1, "Admin")[0]:
        return user
    else:
        return None


@api_view(["POST"])
def auth_register(request):
    if "username" in request.data and "password" in request.data:
        username = request.data["username"]
        password = request.data["password"]
        if username != "" and password != "":
            try:
                Account.objects.get(username=username)
                return Response(status=status.HTTP_409_CONFLICT)
            except ObjectDoesNotExist:
                account = Account(username=username, password=password, register_time=datetime.now())
                if Account.objects.count() == 0:
                    account.group = tuple_search(USER_GROUP, 1, "Admin")[0]
                account.save()
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def auth_login(request):
    if "username" in request.GET and "password" in request.GET:
        username = request.GET["username"]
        password = request.GET["password"]
        if username != "" and password != "":
            try:
                account = Account.objects.get(username=username, password=password)
                if account.banned:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                else:
                    account.ticket = str(uuid.uuid4())
                    account.last_login = datetime.now()
                    account.ip = get_client_ip(request)
                    account.save()
                    resp = {"ticket": account.ticket}
                    Log(account=account, t=datetime.now(), ip=get_client_ip(request), type="auth/login", request=request.GET, response=resp).save()
                    return Response(resp)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def auth_password(request):
    if "username" in request.data and "old" in request.data and "new" in request.data:
        username = request.data["username"]
        password_old = request.data["old"]
        password_new = request.data["new"]
        try:
            account = Account.objects.get(username=username, password=password_old)
            account.password = password_new
            account.last_update = datetime.now()
            account.ticket = None
            account.save()
            Log(account=account, t=datetime.now(), ip=get_client_ip(request), type="auth/password", request=request.data, response=None).save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def auth_verify(request):
    if check_user(request) is not None:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def auth_detail(request):
    user = check_user(request)
    if user is not None:
        return Response(AccountSerializer(user).data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def auth_list(request):
    if check_admin(request) is not None:
        return Response(AccountSerializer(Account.objects.all(), many=True).data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["PUT"])
def auth_modify(request):
    if "username" in request.data and "field" in request.data and "value" in request.data:
        user = check_admin(request)
        if user is not None:
            try:
                account = Account.objects.get(username=request.data["username"])
                setattr(account, request.data["field"], request.data["value"])
                account.save()
                resp = AccountSerializer(account).data
                Log(account=user, t=datetime.now(), ip=get_client_ip(request), type="auth/modify", request=request.data, response=resp).save()
                return Response(resp)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def auth_log(request):
    user = check_user(request)
    if user is not None:
        if "id" in request.GET:
            try:
                if check_admin(request):
                    return Response(LogSerializer(Log.objects.get(id=request.GET["id"])).data)
                else:
                    return Response(LogSerializer(Log.objects.get(id=request.GET["id"], account=user)).data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if check_admin(request):
                if "username" in request.GET:
                    try:
                        account = Account.objects.get(username=request.GET["username"])
                        return Response(LogSerializer(Log.objects.filter(account=account).order_by("t")[:100], many=True).data)
                    except ObjectDoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(LogSerializer(Log.objects.order_by("t")[:100], many=True).data)
            else:
                return Response(LogSerializer(Log.objects.filter(account=user).order_by("t")[:100], many=True).data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
