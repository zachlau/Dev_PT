from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, StreamingHttpResponse
from index.models import *
import xlrd
import zipfile, shutil
from index import util
# Create your views here.

def home(request):
    return render(request, 'home.html')


def base(request):
    return render(request, 'index_base.html')


def index_login(request):
    return render(request, 'login.html')


def index_register(request):
    return render(request, 'register.html')

def user_exist(request):
    username = request.GET.get('username')
    if username in ['admin', 'tianlaoshi', 'zhangsan']:
        return JsonResponse({"flag": True})
    else:
        return JsonResponse({"flag": False})

def api_register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    if username and password and email:
        if len(username) < 10 and len(password) < 10:
            u = Users.objects.filter(username=username)
            e = Users.objects.filter(email=email)
            if not u.exists() and not e.exists():
                Users.objects.create(username=username, password=password, email=email)
                return HttpResponseRedirect('/index/success/')
            else:
                info = "用户名或邮箱已存在"
        else:
            info = "用户名密码位数错误"
    else:
        info = "缺少必填参数"
    return render(request, 'error.html', {"info": info})

def success(request):
    return render(request, 'success.html')

# def api_login(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")
#     if username and password:
#         if len(username) < 10 and len(password) < 10:
#             u = Users.objects.filter(username=username, password=password)
#             if u.exists():
#                 return HttpResponseRedirect('/index/demo/')
#             else:
#                 info = "用户名或密码错误"
#         else:
#             info = "用户名密码位数错误"
#     else:
#         info = "缺少必填参数"
#     return render(request, 'error.html', {"info": info})

def api_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username and password:
        if len(username) < 10 and len(password) < 10:
            u = Users.objects.filter(username=username, password=password)
            if u.exists():
                return JsonResponse({"flag": True})
            else:
                info = "用户名或密码错误"
        else:
            info = "用户名密码位数错误"
    else:
        info = "缺少必填参数"
    return JsonResponse({"flag": False, "info": info})


def index_task(request):
    tasks = Task.objects.filter(avalible=1).values('id', 'name', 'project__name', 'category', 'user__username', 'status')
    projects = Project.objects.all()
    return render(request, 'task.html', {"tasks": tasks, "projects": projects})

def index_newtask(request):
    projects = Project.objects.all()
    users = Users.objects.all()
    return render(request, 'task_new.html', {"projects": projects, "users": users})

def task_exist(request):
    name = request.GET.get('name')
    flag = False
    if Task.objects.filter(name=name).exists():
        flag = True
    return JsonResponse({"flag": flag})

def api_newtask(request):
    name = request.POST.get('name')
    project = request.POST.get('project')
    category = request.POST.get('category')
    user = request.POST.get('user')
    status = request.POST.get('status')
    if name and project and category and user and status:
        if not Task.objects.filter(name=name).exists():
            Task.objects.create(name=name, project_id=int(project), category=int(category),
                                user_id=int(user), status=int(status))
            return HttpResponseRedirect('/index/task/')
        else:
            info = "需求已存在"
    else:
        info = "缺少必填参数"
    return render(request, 'error.html', {"info": info})

def api_gettask(request):
    project = request.GET.get('project')
    keyword = request.GET.get('keyword')
    # 两个都有
    if  project and  keyword:
        if project != "0":
            tasks = Task.objects.filter(project_id=int(project), name__contains=keyword, avalible=1).values('id', 'name', 'project__name', 'category', 'user__username', 'status')
        else:
            tasks =Task.objects.filter(name__contains=keyword, avalible=1).values('id', 'name', 'project__name', 'category', 'user__username', 'status')
    # 有project一个
    elif project and not keyword:
        if project != "0":
            tasks =Task.objects.filter(project_id=int(project), avalible=1).values('id', 'name', 'project__name', 'category', 'user__username', 'status')
        else:
            tasks =Task.objects.filter(avalible=1).values('id', 'name', 'project__name', 'category', 'user__username', 'status')
    # 有keyword一个
    elif not project and keyword:
        tasks =Task.objects.filter(name__contains=keyword, avalible=1).values('id', 'name', 'project__name', 'category', 'user__username', 'status')
    # 两个都没有
    else:
        tasks =Task.objects.filter(avalible=1).values('id', 'name', 'project__name', 'category', 'user__username', 'status')
    print({"tasks": list(tasks)})
    return JsonResponse({"tasks": list(tasks)})


def api_deletetask(request):
    pid = request.GET.get('pid')
    if pid:
        try:
            Task.objects.filter(id=pid).delete()
        except:
            flag = False
        flag = True
    else:
        flag = False
    return JsonResponse({"flag": flag})

def api_guidangtask(request):
    pid = request.GET.get('pid')
    if pid:
        tasks = Task.objects.filter(id=pid)
        if tasks.exists():
            task = tasks.first()
            task.avalible = 0
            task.save()
        else:
            flag = False
        flag = True
    else:
        flag = False
    return JsonResponse({"flag": flag})

def index_updatetask(request):
    pid = request.GET.get('pid')
    projects = Project.objects.all()
    users = Users.objects.all()
    if pid:
        tasks = Task.objects.filter(id=pid)
        if tasks.exists():
            return render(request, 'task_update.html', {"task": tasks.first(), "projects": projects, "users": users})

def apitest(request):
    return render(request, 'apitest.html')


def api_uploadcases(request):
    file = request.FILES.get('case_file')
    p = open('./files/'+file.name, 'wb')
    for f in file.chunks():
        p.write(f)
    p.close()
    try:
        workbook = xlrd.open_workbook('./files/'+file.name)
        sheet = workbook.sheet_by_index(0)
        count = 0
        for i in range(1, sheet.nrows):
            #导入数据库
            data = sheet.row_values(i)
            number = data[0]
            desc = data[1]
            url = data[2]
            method = data[3]
            headers = data[4]
            type = data[5]
            body = data[6]
            checks = data[7]
            if number and desc and url and method and checks:
                if not Cases.objects.filter(number=number).exists():
                    try:
                        Cases.objects.create(number=number, desc=desc, url=url, method=method,
                                             headers=headers, type=type, body=body, checks=checks)
                        count += 1
                    except:
                        continue
        if count > 0:
            return render(request, 'success.html', {"info": "成功导入%d个测试用例" % count, "link": "/index/cases/"})
        else:
            return render(request, 'error.html', {"info": "本次未能导入有效的测试用例，请检查excel文件内容", "link": "/index/apitest/"})
    except:
        return render(request, 'error.html', {"info": "用例文件格式非有效的excel", "link": "/index/apitest/"})


def index_cases(request):
    cases = Cases.objects.all()
    return render(request, 'cases.html', {"cases": cases})

def api_run_cases(request):
    case_list = []
    flag = False
    url = ''
    ids = request.POST.get("ids")
    if ids:
        for id in ids.split('&'):
            case = Cases.objects.filter(id=id)
            if case.exists():
                case = case.first()
                data = {}
                data['id'] = case.number
                data['desc'] = case.desc
                data['url'] = case.url
                data['method'] = case.method
                data['headers'] = case.headers
                data['body_type'] = case.type
                data['body_value'] = case.body
                data['checks'] = case.checks
                case_list.append(data)
        url = util.start_run(case_list)
        if url:
            flag = True
    return JsonResponse({"flag": flag, "url": url})

def index_apk(request):
    return render(request, 'apk.html')

def api_upload_apk(request):
    flag = False
    try:
        file = request.FILES.get('apk_file')
        p = open('./files/apk/'+file.name, 'wb')
        for f in file.chunks():
            p.write(f)
        p.close()
        flag = True
        name = file.name
    except:
        name = ''
        pass
    return JsonResponse({"flag": flag, 'name': name})

def api_run_apk(request):
    name = request.POST.get('file_name')
    qudao = request.POST.get('qudao')
    if name and qudao:
        try:
            shutil.copy("./files/apk/%s" % name, './files/finish/%s.apk' % qudao)
            zipped = zipfile.ZipFile('./files/finish/%s.apk' % qudao, 'a', zipfile.ZIP_DEFLATED)
            empty_channel_file = "META-INF/wzchannel_{channel}".format(channel=qudao)
            zipped.write("./files/apk/empty_file", empty_channel_file)
            zipped.close()
            response = StreamingHttpResponse(open('./files/finish/%s.apk' % qudao, 'rb'))
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment;filename={0}'.format('%s.apk' % qudao)
            return response
        except Exception as e:
            print(e)
    return render(request, 'error.html', {"info": "打包失败！", "link": "/index/apk/"})