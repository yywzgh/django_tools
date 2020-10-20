from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from rediscluster import RedisCluster
from rediscluster.exceptions import RedisClusterException
from functools import wraps
from django.shortcuts import render
from . import constant
from django_tools.models import UserInfo
import pymysql
import os
import json
import paramiko
from urllib import parse
import xlrd
import xlwt
from xlutils.copy import copy
from django.http import StreamingHttpResponse

def check_login(f):
    @wraps(f)
    def inner(request, *arg, **kwargs):
        if request.session.get('is_login') == '1':
            return f(request, *arg, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner


def login(request):
    # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserInfo.objects.filter(username=username, password=password)

        print("login action")
        if user:
            #登录成功
            # 1，生成特殊字符串
            # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
            # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
            request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
            request.session['username'] = username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
            # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
            request.session['user_id'] = user[0].id
            return render(request, '/')
    # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request, 'login.html')


def handle_404(request, exception):
    return render(request, '404.html')


def handle_500(request):
    return render(request, '500.html')


#@check_login
def index(request):
    #template = loader.get_template('index.html')
    #context = {
    #    'redis_keys': [],
    #}
    #return HttpResponse(template.render(context, request))
    return render(request, 'index.html')


def head(request):
    return render(request, 'head.html')


def query_key(request):

    message = ""
    env_type = request.POST.get('envType')
    param = request.POST.get('key')
    flag = request.POST.get('flag')
    redis_nodes = []
    list_keys = ['']

    if env_type is not None:
        redis_nodes = constant.Const.redis_nodes_dict().get(env_type)
    else:
        return HttpResponseRedirect('/')

    try:
        redis_conn = RedisCluster(startup_nodes=redis_nodes, decode_responses=False)
    except RedisClusterException:
        message = "连接Redis服务失败！"
        context = {
            'redis_keys': list_keys,
            'key': param,
            'env_type': env_type,
            'message': message
        }
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
    else:
        list_keys = redis_conn.keys("*" + param + "*")

    if flag == "0" and param is not None:
        for keys in list_keys:
            redis_conn.delete(keys)
        message = "删除成功！"
        list_keys = ['']

    if flag == "1" and len(list_keys) == 0:
        message = "没有查询结果！"

    context = {
        'redis_keys': list_keys,
        'key': param,
        'env_type': env_type,
        'message': message
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def clean_user_info(request):

    phone_number = request.POST.get('phoneNumber')
    env_type = request.POST.get('envType')
    flag = request.POST.get('flag')

    if phone_number is None:
        context = {}
        template = loader.get_template('user.html')
        return HttpResponse(template.render(context, request))

    mysql_dict = constant.Const.mysql_nodes_dict().get(env_type)

    conn = pymysql.connect(**mysql_dict)

    cursor = conn.cursor()

    sql = "select user_id, user_name, phonenumber, sessionid, invite_code from sys_user where phonenumber=%s;"
    cursor.execute(sql, [phone_number])
    ret = cursor.fetchone()
    cursor.close()
    conn.close()

    if ret is None:
        context = {'message': "用户不存在"}
        template = loader.get_template('user.html')
        return HttpResponse(template.render(context, request))

    user_id = ret[0]
    user_name = ret[1]
    phone_number = ret[2]
    session_id = ret[3]
    invite_code = ret[4]

    if flag == "0":
        redis_nodes = constant.Const.redis_nodes_dict().get(env_type)
        redis_conn = RedisCluster(startup_nodes=redis_nodes)

        user_id_keys = redis_conn.keys("*" + str(user_id) + "*")
        for keys in user_id_keys:
            redis_conn.delete(keys)

        user_name_keys = redis_conn.keys("*" + user_name + "*")
        for keys in user_name_keys:
            redis_conn.delete(keys)

        phone_number_keys = redis_conn.keys("*" + phone_number + "*")
        for keys in phone_number_keys:
            redis_conn.delete(keys)

        session_id_keys = redis_conn.keys("*" + session_id + "*")
        for keys in session_id_keys:
            redis_conn.delete(keys)

        invite_code_keys = redis_conn.keys("User:invitecode:" + invite_code)
        for keys in invite_code_keys:
            redis_conn.delete(keys)

        message = "用户redis缓存删除成功！"
        context = {'message': message}
        template = loader.get_template('user.html')
        return HttpResponse(template.render(context, request))

    context = {
        'env_type': env_type,
        'user_id': user_id,
        'user_name': user_name,
        'phone_number': phone_number,
        'session_id': session_id,
        'invite_code': invite_code,
    }

    template = loader.get_template('user.html')
    return HttpResponse(template.render(context, request))


def server_info(request):
    template = loader.get_template('server.html')
    return HttpResponse(template.render({}, request))


def server_jc(request):
    template = loader.get_template('server_jc.html')
    return HttpResponse(template.render({}, request))


def upload_view(request):
    return render(request, 'upload.html')


def upload_file(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        print(myFile.name)
        if not myFile:
            result = {"msg": "请选择要上传的文件", "result": True}
            return HttpResponse(json.dumps(result));
        destination = open(os.path.join("/tmp", myFile.name), '+wb');
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        os.system("rm -rf /tmp/data/*")
        os.system("unzip /tmp/nginx-1.18.0.zip -d /tmp/data/")
        result = {"msg": "上传成功", "result": True}
        return HttpResponse(json.dumps(result))




def exec_shell():
    ssh = paramiko.SSHClient()
    # 创建一个ssh的白名单
    know_host = paramiko.AutoAddPolicy()
    # 加载创建的白名单
    ssh.set_missing_host_key_policy(know_host)

    # 连接服务器
    ssh.connect(
        hostname="10.10.21.177",
        port=22,
        username="root",
        password="123"
    )

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command("rm -rf /root/Desktop/mv")
    # stdin  标准格式的输入，是一个写权限的文件对象
    # stdout 标准格式的输出，是一个读权限的文件对象
    # stderr 标准格式的错误，是一个写权限的文件对象

    print(stdout.read().decode())
    ssh.close()

def create_new_excel(filename):
    jsRet = 'http://s.click.taobao.com/t?e=m%3D2%26s%3DqhJAcX7%2Bvrhw4vFB6t2Z2iperVdZeJvif3ovRFFLMflyINtkUhsv0Ew%2BhbtSTsKNl98B4vYpthEWf0dXEcisqxuW%2F4tFxi4k2AO0BTh9f1Ro6mKT%2F0Nw9GCjIPCBLYBG3m4QuH8jCk%2BhNGov5IhV8dsZBKmFwI6UXXTsZUpItSdkxUN95Rfe9t6Fvf5jtf3KfIrCKoPZYrQGZ%2FstJHrpqHFgO2kTJ5OG47FHjfsActlyU3PkLHqE2KEfqx389mdY283URdPsIygrRhC7UydvEj4McANQIq1sJNLR%2BromdVzIYIn%2FaSXwsjMd8ymktK03xiXvDf8DaRs%3D&union_lens=lensId%3APUB%401601184994%400b50fd1e_0d84_174ce101463_0e28%4001&direct_sale=1'
    #print(parse.unquote(jsRet))  # 输出：中国

    tbopen = "tbopen://m.taobao.com/tbopen/index.html?action=ali.open.nav&module=h5&h5Url="

    print(tbopen + parse.quote(jsRet))  # 输出：True
    dat = []
    dat = read_excel(filename)
    modify_excel(dat,filename)
    #return HttpResponse(json.dumps(result))
    #return render(request, 'upload.html')


def upload_excel_view(request):
    return render(request, 'upload_excel.html')


def upload_excel(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile", None)
        print(myFile.name)
        if not myFile:
            result = {"msg": "请选择要上传的文件", "result": True}
            return HttpResponse(json.dumps(result));
        destination = open(os.path.join("upload/", myFile.name), '+wb');
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        result = {"msg": "上传成功", "result": True}
        create_new_excel(myFile.name)
        return HttpResponse(json.dumps(result))


def read_excel(filename):
    wb = xlrd.open_workbook('upload/'+filename)# 打开Excel文件
    sheet = wb.sheet_by_index(0)#通过excel表格名称(rank)获取工作表
    dat = []  #创建空list
    tbopen = "tbopen://m.taobao.com/tbopen/index.html?action=ali.open.nav&module=h5&h5Url="
    for a in range(sheet.nrows):  #循环读取表格内容（每次读取一行数据）
        if a > 0:
            cells = sheet.row_values(a)  # 每行数据赋值给cells
            data=cells[1]#因为表内可能存在多列数据，0代表第一列数据，1代表第二列，以此类推
            print(tbopen + parse.quote(data))
            dat.append(tbopen + parse.quote(data)) #把每次循环读取的数据插入到list
    total = len(dat)
    return dat


def write_excel():
    wb = xlwt.Workbook(encoding = 'ascii')  #创建新的Excel（新的workbook），建议还是用ascii编码
    sheet = wb.sheet_by_name('becks')#通过excel表格名称(rank)获取工作表
    for a in range(sheet.nrows):
        ws = wb.add_sheet('weng')               #创建新的表单weng
        ws.write(0, 0, label = 'hello')         #在（0,0）加入hello
        ws.write(0, 1, label = 'world')         #在（0,1）加入world
        ws.write(1, 0, label = '你好')
    wb.save('weng.xls')


def modify_excel(data_list, filename):
    # xlutils:修改excel
    new_excel = xlrd.open_workbook('upload/'+filename)
    book2 = copy(new_excel)  # 拷贝一份原来的excel
    sheet = book2.get_sheet(0)  # 获取第几个sheet页，book2现在的是xlutils里的方法，不是xlrd的
    for inx, li in enumerate(data_list):
        sheet.write(inx + 1, 2, li)
    book2.save("upload/new-"+filename)


def download_excel(request, filename):
    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name ="upload/new-" + filename #要下载的文件路径
    response =StreamingHttpResponse(file_iterator(the_file_name))#这里创建返回
    response['Content-Type'] = 'application/vnd.ms-excel'#注意格式
    response['Content-Disposition'] = 'attachment;filename="weibo.xls"'#注意filename 这个是下载后的名字
    return response