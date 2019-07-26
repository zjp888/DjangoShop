from django.urls import path
from django.urls import re_path
from FreshApp.views import *

urlpatterns = [
    path("register/",register),
    path("login/",login),
    path("index/",index),
    path("logout/",logout),
    path("base/",base),
    path("register_store/",register_store),
    path("add_goods/",add_goods),
    re_path(r"list_goods/(?P<state>\w+)",list_goods),
    re_path(r"^goods/(?P<goods_id>\d+)",goods),
    re_path(r"update_goods/(?P<goods_id>\d+)",update_goods),
    re_path(r'set_goods/(?P<state>\w+)/', set_goods), #设置商品状态
    path("list_goods_type/",list_goods_type),
    path("delete_goods_type/",delete_goods_type),

]
