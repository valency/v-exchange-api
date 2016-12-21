from django.conf.urls import url

from vex_auth import views

urlpatterns = [
    url(r"register/$", views.auth_register),
    url(r"login/$", views.auth_login),
    url(r"password/$", views.auth_password),
    url(r"verify/$", views.auth_verify),
    url(r"detail/$", views.auth_detail),
    url(r"list/$", views.auth_list),
    url(r"modify/$", views.auth_modify),
    url(r"log/$", views.auth_log)
]
