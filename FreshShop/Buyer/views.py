from alipay import AliPay
import hashlib
import time

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from FreshApp.models import *
# Create your views here.
#对密码进行加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

#验证cookies和session是否正确
def loginVaild(fun):
    def inner(request,*args,**kwargs):
        u_cookies = request.COOKIES.get("username")
        s_session = request.session.get("username")
        if u_cookies and s_session and u_cookies == s_session:
            return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/buyer/login")
    return inner

#可有可没有
def base(request):
    return render(request,"buyer/base.html",locals())

#v1.0注册功能实现
#v1.1加密完成
def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        if username and password:
            buyer = Buyer()
            buyer.username = username
            buyer.password = setPassword(password)
            buyer.email = email
            buyer.save()
        return HttpResponseRedirect('/buyer/login/')
    return render(request,"buyer/register.html",locals())

#登录功能实现加密完成
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            if user:
                web_password = setPassword(password)
                if user.password == web_password:
                    response = HttpResponseRedirect("/buyer/index/")
                    response.set_cookie("username",user.username)
                    request.session["username"] = user.username
                    response.set_cookie("user_id",user.id)
                    return response

    return render(request,"buyer/login.html",locals())

#登录首页
@loginVaild
def index(request):
    result_list = []#定义一个容器来存放结果
    goods_type_list = GoodsType.objects.all()
    for goods_type in goods_type_list:#循环类型
        goods_list = goods_type.goods_set.values()[:4]#展示出前4个
        if goods_type:#如果类型对应的商品有值
            #封装到一个新的字典中方便展示数据
            goods_type = {
                "id":goods_type.id,
                "name":goods_type.name,
                "description": goods_type.description,
                "picture": goods_type.picture,
                "goods_list": goods_list,
            }#构建输出结果
            #查询类型当中所有的数据
            result_list.append(goods_type)#有数据的类型放入result_list
    return render(request,"buyer/index.html",locals())
#商品详情页
def goods_detail(request):
    goods_id = request.GET.get("goods_id")
    if goods_id:
        goods = Goods.objects.filter(id=goods_id).first()
        if goods:
             return render(request,"buyer/detail.html",locals())
    return HttpResponse("没有找到指定的商品")


@loginVaild
def goods_list(request):
    """
    前台列表页展示
    """
    goodsList = []
    type_id = request.GET.get("type_id")
    #获取类型
    goods_type = GoodsType.objects.filter(id = type_id).first()
    if goods_type:
        #查询所有上架商品
        goodsList = goods_type.goods_set.filter(goods_under=1)
    return render(request,"buyer/goods_list.html",locals())
#退出功能实现
def logout(request):
    response = HttpResponseRedirect("/buyer/login/")
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response

#设置订单号时间+用户id，商品id，商铺id
def setOrderId(user_id,goods_id,store_id):
    strtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return str(strtime)+str(user_id)+str(goods_id)+str(store_id)


#购买的详情
def place_order(request):
    if request.method == "POST":
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        user_id = request.COOKIES.get("user_id")
        goods = Goods.objects.get(id=goods_id)
        store_id = goods.store_id.id
        price = goods.goods_price
        order = Order()
        order.order_id = setOrderId(str(user_id),str(goods_id),str(store_id))
        order.goods_count = count
        order.order_user = Buyer.objects.get(id=user_id)
        order.order_price = count * price
        order.save()
        order_detail = OrderDetail()
        order_detail.order_id = order
        order_detail.goods_id = goods_id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_price = goods.goods_price
        order_detail.goods_number = count
        order_detail.goods_total = count * goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_image = goods.goods_image
        order_detail.save()
        detail = [order_detail]
        return render(request, "buyer/place_order.html", locals())
    else:
        order_id = request.GET.get("order_id")
        if order_id:
            order = Order.objects.get(id=order_id)
            detail = order.orderdetail_set.all()
            return render(request, "buyer/place_order.html", locals())
        else:
            return HttpResponse("非法请求")
#购物车
def cart(request):
    user_id = request.COOKIES.get("user_id")
    goods_list = Cart.objects.filter(user_id=user_id)
    if request.method == "POST":
        post_data = request.POST
        cart_data = []
        for k,v in post_data.items():
            if k.startswith("goods_"):
                cart_data.append(Cart.objects.get(id=int(v)))
        goods_count = len(cart_data)
        goods_total = sum(([int(i.goods_total) for i in cart_data]))
        #保存订单
        order = Order()
        # 订单当中有多个商品或者多个店铺，使用goods_count来代替商品id，用2代替店铺id
        order.order_id = setOrderId(user_id,goods_count,"2")
        order.goods_count = goods_count
        order.order_user = Buyer.objects.get(id=user_id)
        order.order_price = goods_total
        order.order_status = 1
        order.save()
        # 保存订单详情
        # 这里的detail是购物车里的数据实例，不是商品的实例
        for detail in cart_data:
            order_detail = OrderDetail()
            order_detail.order_id = order  # order是一条订单数据
            order_detail.goods_id = detail.goods_id
            order_detail.goods_name = detail.goods_name
            order_detail.goods_price = detail.goods_price
            order_detail.goods_number = detail.goods_number
            order_detail.goods_total = detail.goods_total
            order_detail.goods_store = detail.goods_store
            order_detail.goods_image = detail.goods_picture
            order_detail.save()
        # order是一条订单支付页
        url = "/buyer/place_order/?order_id=%s"%order.id
        return HttpResponseRedirect(url)
    return render(request,"buyer/cart.html",locals())
#添加购物车
def add_cart(request):
    result = {"status":"error","data":""}
    if request.method == "POST":
        count = int(request.POST.get("count"))
        print(count)
        goods_id = request.POST.get("goods_id")
        goods = Goods.objects.get(id=int(goods_id))
        user_id = request.COOKIES.get("user_id")
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price * count
        cart.goods_number = count
        cart.goods_picture= goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store_id.id
        cart.user_id = user_id
        cart.save()
        result["status"] = "success"
        result["data"] = "商品添加成功"
    else:
        result["data"] = "请求错误"
    return JsonResponse(result)



def pay_result(request):
    """
    支付宝支付成功自动用get请求返回的参数
    #编码
    charset=utf-8
    #订单号
    out_trade_no=10002
    #订单类型
    method=alipay.trade.page.pay.return
    #订单金额
    total_amount=1000.00
    #校验值
    sign=enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D&trade_no=2019072622001422161000050134&auth_app_id=2016093000628355&version=1.0&app_id=2016093000628355
    #订单号
    trade_no=2019072622001422161000050134
    #用户的应用id
    auth_app_id=2016093000628355
    #版本
    version=1.0
    #商家的应用id
    app_id=2016093000628355
    #加密方式
    sign_type=RSA2
    #商家id
    seller_id=2088102177891440
    #时间
    timestamp=2019-07-26
    """
    return render(request,"buyer/pay_result.html", locals())

def pay_order(request):
    money = request.GET.get("money")  # 获取订单金额
    order_id = request.GET.get("order_id")  # 获取订单id

    alipay_public_key_string ="""-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwqdG6DlyVk0JEKB34cFYn48WpcqtsGLEbIs8oXJNFstuWLHspAmBnIlrr7ljD8spaj/3Cz0G+493tuC8fiejxc3spHj4z833EYFWlbhu+nenr0aCPBFtq1o7AYpTpXIZjXBf6roHiYTbQjD9Vws3fr5JmVTRNkcHc6/P3Bv4RxP/kjFuLcABximakYsinCJ2vg1SLI+ADdlcfln/9RIqkyrKekck491rpsIeTA2meyCgMTSJExEDMsWDFw+mmYvMPqKVxOFbkitNv1vEdS+Ucm+8i8yzrIapWGpLtavyA2591+BiffCxoZhL+RgFRVxuOzHOn5YZe+EwxJ4YsPWjLwIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string ="""-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAwqdG6DlyVk0JEKB34cFYn48WpcqtsGLEbIs8oXJNFstuWLHspAmBnIlrr7ljD8spaj/3Cz0G+493tuC8fiejxc3spHj4z833EYFWlbhu+nenr0aCPBFtq1o7AYpTpXIZjXBf6roHiYTbQjD9Vws3fr5JmVTRNkcHc6/P3Bv4RxP/kjFuLcABximakYsinCJ2vg1SLI+ADdlcfln/9RIqkyrKekck491rpsIeTA2meyCgMTSJExEDMsWDFw+mmYvMPqKVxOFbkitNv1vEdS+Ucm+8i8yzrIapWGpLtavyA2591+BiffCxoZhL+RgFRVxuOzHOn5YZe+EwxJ4YsPWjLwIDAQABAoIBAGTsznsBriLI9nZEfWP0F7tDOX7kw4G89BNDbkBXP1keSSx7tDKpKya6qbcG7DH4KJUKbVDKZ6BvFqcfhxvx+ZxJ1PTCNF+qbvwIj5g5dHExMSRT7pqufqplskpuKkiSDGWlalYN9nJ7DCQZuoEzM6bnismRjJgT4+07rw51Ahn3gQJ3W3vkhaRbpOP57t7bhZSNuVcv4O99INrlrJeF6pKN5RDOqHjEV6cdi08iApADXZUaJqPOLGkymiZkHf7b5lcv44knWKrWI8xs/8G/9en8BWHPcTPMD5Ml1exdRyDECaTiFd/qKH+fWSCxuwqgl56nBcKQ8ChMbCMenNsvlIECgYEA4FS4Df4ACP5VlLMXd6oh4x99BLfJel3qML0DhrXHInVGCgshlUeXzwOB8MLpqDFKf7kiGD9Wjc7x4nRr/OPBlmkts3a/ma35mX2mRvC0embuqXwaBfrYAI2+aeVMF2mQE36GmXGNjTje6ciNIm+nRYAE3RtokuT42cJEv2kEU5ECgYEA3iIEndlhwc6ZVwbAbmW79IEJSCU8scPWk+7acLW8gXfnhupfUiN7s6KUJZrhYaEnevZH7talNiP6LPApGXW1Mme/PNLyZqe4sNUBMGFgEqWphVna2zv+fiA+yLHSu9j6g3mY/RO9dG9qVTNxseRqng3Jbu2Cwhj3rO23OHrtqr8CgYBv6ROgt1PhKLAc7HMKmW8qVO0TS3RRfUR1Z/W4YDqlcAeuvvrT89FBzqgmKbZS17Qon3zox8AwIkr9A8NTd3N9y56m5tiSm/3mmo422aHPZkYteuGolgjnzc5uGZuqGllrwDT5m3JYP0TFL+1ofnbd7w1+GExE68FRMN8G9ibYYQKBgFmBLYkI+WnlPEYjs1AIcBaSE9JdJrqeJY0QFjaKE/26+bCUKXpoT8TPApCwepYjIExchhmHpaROFNUcpALdOfiocxcoDIIunK2r9kGvSs3YsJjJ3vStlNrvVTz64eXNBQwK6Ak5dgI/joHsK6i5V/h9p6epziE1fD7Svhvk9HTzAoGBALXmpgkHMxqLvH8oIh4E2E9H1l804Nha/vxsSIkh6Ef+h3mcjIAquGKw+nHKfXzohaOnvRj+N15vxPnCvT1WXHUAOYI/exgjZRoswJh9JT/pOOUJkLqAcLqH3L9D+8VswyeGBJzQkHrsVFTe5lAqIRZuO9Hw3AIqXAzuEJHJCbOG
    -----END RSA PRIVATE KEY-----"""

    # 实例化支付应用
    alipay = AliPay(
        appid="2016101000652516",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主题
        return_url="http://127.0.0.1:8000/buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/buyer/pay_result/",
    )

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?"+order_string)

def base_zhifu(request):
    return render(request,"buyer/base_zhifu.html")

