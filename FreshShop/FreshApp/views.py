import hashlib
from FreshApp.models import *
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
                    return response
    return response

@loginVaild
def index(request):

    return render(request,"freshApp/index.html",locals())