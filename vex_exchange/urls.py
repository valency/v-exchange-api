from django.conf.urls import url

from vex_exchange import views

urlpatterns = [
    url(r'stock/$', views.stock)
]
