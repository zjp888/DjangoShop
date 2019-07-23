import hashlib
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from FreshApp.models import *

# Create your views here.
#对用户的密码进行加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

#定义装饰器来校验首页列表
def loginVaild(fun):
    def inner(request,*args,**kwargs):
        u_cookies = request.COOKIES.get("username")
        s_session = request.session.get("username")
        if u_cookies and s_session and u_cookies == s_session:
            user = Seller.objects.filter(username=u_cookies).first()
            if user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/fresh/login')
    return inner
#用户注册
def register(request):
    """
    register注册
    返回注册页面
    进行注册数据保存
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            seller = Seller()
            seller.username = username
            seller.password = setPassword(password)
            seller.nickname = username
            seller.save()
            return HttpResponseRedirect("/fresh/login/")
    return render(request,"freshApp/register.html",locals())

def login(request):
    """
    登录功能，如果登录成功，跳转到首页
    如果失败，跳转到登录页
    """
    response = render(request,"freshApp/login.html",locals())
    response.set_cookie("login_form","login_page")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if user:
                web_password = setPassword(password)
                cookies = request.COOKIES.get("login_form")
                if user.password == web_password and cookies == "login_page":
                    response = HttpResponseRedirect("/fresh/index")
                    response.set_cookie("username",username)
                    request.session["username"] = username
                    response.set_cookie("user_id",user.id)#cookie提供用户id方便其他功能查询
                    return response
    return response

@loginVaild
def index(request):
    """
    检查账号是否有店铺
    """
    #查询当前用户是谁
    user_id = request.COOKIES.get("user_id")
    if user_id:
        user_id = int(user_id)
    else:
        user_id = 0
    #通过用户查询店铺是否存在(店铺和用户之间用id进行关联)
    store = Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request,"freshApp/index.html",{"is_store":is_store})

#base页
def base(request):
    return render(request,"freshApp/base.html",locals())

def register_store(request):
    type_list = StoreType.objects.all()
    if request.method == "POST":
        post_data = request.POST
        store_name = post_data.get("store_name")
        store_address = post_data.get("store_address")
        store_descripton = post_data.get("store_descripton")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")

        user_id = int(request.COOKIES.get("user_id"))
        type_lists = post_data.getlist("type")
        store_logo = request.FILES.get("store_logo")
        store = Store()
        store.store_name = store_name
        store.store_address = store_address
        store.store_descripton = store_descripton
        store.store_phone = store_phone
        store.store_money = store_money
        store.user_id = user_id
        store.store_logo = store_logo
        store.save()

        for i in type_lists:
            store_type = StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
    return render(request,"freshApp/register_store.html",locals())


def add_goods(request):
    """
    负责添加商品
    """
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.POST.get("goods_store")
        goods_image = request.FILES.get("goods_image")
        #开始保存数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()

        #保存多对多数据
        goods.store_id.add(
            Store.objects.get(id=int(goods_store))
        )
        goods.save()
    return render(request,"freshApp/add_goods.html",locals())

#商品以形式展开列表
def list_goods(request):

    #判断如果搜索不为空的情况下
    keywords = request.GET.get("keywords","")
    page_unm = request.GET.get("page_unm",1)
   #返回上一页的地址和关键字
    referer = request.META.get("'HTTP_REFERER'")
    if keywords:
        goods_list = Goods.objects.filter(goods_name__contains=keywords)
    else:
        if referer and "?" in referer:
            get_str = referer.split("?")[1]
            get_list = [i.split("=") for i in get_str.split("&")]
            get_dict = dict(get_list)
            if "keyword" in get_dict:
                keywords = get_dict["keywords"]
            goods_list = Goods.objects.filter(goods_name__contains=keywords)
        else:
            goods_list = Goods.objects.all()

    # if keywords:
    #     #完成的模糊查询
    #     if keywords in referer:
    #         goods_list = Goods.objects.filter(goods_name__contains=keywords)
    # else:
    #     #如果没有的话返回所有的列表
    #     goods_list = Goods.objects.all()
    paginator = Paginator(goods_list,3)
    page = paginator.page(int(page_unm))
    page_range = paginator.page_range
    return render(request,"freshApp/list_goods.html",locals())