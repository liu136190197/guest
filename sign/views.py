from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from sign.models import Event,Guest

# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request, "index.html")
#登录
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        '''使用 authenticate()函数认证给出的用户名和密码。它接受两个参数，用户名 username 和密码 password，
        并在用户名密码正确的情况下返回一个 user 对象。如果用户名密码不正确，则 authenticate()返回 None。'''
        if user is not None:
            auth.login(request, user)  # 登录
            #return HttpResponse('login success!')
            response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user', username, 3600)  # 添加浏览器 cookie
            request.session['user'] = username  # 将 session 信息记录到浏览器
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    else:
        return render(request, 'index.html', {'error': 'request.method is not post'})
# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response
# 发布会管理
@login_required
def event_manage(request):
    #username = request.COOKIES.get('user', '')  # 读取浏览器 cookie
    event_list = Event.objects.all()
    username = request.session.get('user', '')  # 读取浏览器 session
    return render(request, "event_manage.html", {"user": username,
                                                 "events":event_list
                                                 })
# 签到页面
@login_required
def sign_index(request, event_id):
    username = request.session.get('user', '')  # 读取浏览器 session
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {
                                                "user": username,
                                                "event": event})
# 签到动作
@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                               'hint': 'sign in success!',
                                               'guest': result})
# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 5)
    #把查询出来的所有嘉宾列表 guest_list 放到 Paginator 类中，划分每页显示 2 条数据
    page = request.GET.get('page')
    #通过 GET 请求得到当前要显示第几页的数据。
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,
                                             "guests": contacts})

# 发布会名称搜索
@login_required
def search_name_event(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})
# 嘉宾名称搜索
@login_required
def search_name_guest(request):
    username = request.session.get('user', '')
    search_realname = request.GET.get("realname", "")
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})
