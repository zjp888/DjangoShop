from rest_framework import serializers
from FreshApp.models import *

class UserSerializers(serializers.HyperlinkedModelSerializer):
    """声明数据"""
    class Meta:#元数据
        model = Goods #要进行接口话序列的模型
        fields = ["goods_name","goods_price","goods_number","goods_description","goods_safeDate","goods_date"]#返回序列化的字段

class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    """声明查询的表和返回的字段"""
    class Meta:
        model = GoodsType
        fields = ["name","description"]
