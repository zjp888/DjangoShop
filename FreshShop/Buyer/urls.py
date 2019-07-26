from django.urls import path
from Buyer.views import *
urlpatterns = [
    path("register/",register),
    path("login/",login),
    path("index/",index),
    path("logout/",logout),
    path("goods_list/",goods_list),
]

urlpatterns+=[
    path("base/", base),
    path("pay_order/", pay_order),
    path("pay_result/", pay_result),
]
