from django.urls import path
from django.urls import re_path
from FreshApp.views import *

urlpatterns = [
    path("register/",register),
    path("login/",login),
    path("index/",index),
    path("base/",base),
    path("register_store/",register_store),
    path("add_goods/",add_goods),
    path("list_goods/",list_goods),
    re_path(r"^goods/(?P<goods_id>\d+)",goods),
    re_path(r"update_goods/(?P<goods_id>\d+)",update_goods),
]
