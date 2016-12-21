from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^auth/", include("vex_auth.urls")),
    url(r"^stock/", include("vex_stock.urls")),
    url(r"^exchange/", include("vex_exchange.urls"))
]
