from django.urls import path
from Buyer.views import *
urlpatterns = [
    path("register/",register),
    path("login/",login),
    path("index/",index),
    path("logout/",logout),
    path("goods_list/",goods_list),
    path("goods_detail/",goods_detail),
    path("place_order/",place_order),
    path("cart/",cart),
    path("add_cart/",add_cart),
]

urlpatterns+=[
    path("base/", base),
    path("pay_order/", pay_order),
    path("pay_result/", pay_result),
    path("base_zhifu/", base_zhifu),
    path("get_add/", get_add),
]
