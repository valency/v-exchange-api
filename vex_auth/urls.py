from django.conf.urls import url

from vex_auth import views

urlpatterns = [
    # ------- Multiple User Management (Admin Only) -------
    url(r'admin/list/$', views.admin_list),
    url(r'admin/modify/$', views.admin_modify),
    # ------- Single User Management -------
    url(r'login/$', views.login),
    url(r'register/$', views.register),
    url(r'password/$', views.change_password),
    url(r'verify/$', views.verify),
    url(r'detail/$', views.detail),
    # ------- Misc. -------
    url(r'log/$', views.log)
]
