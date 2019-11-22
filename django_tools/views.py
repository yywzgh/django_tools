from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from rediscluster import RedisCluster
from . import constant

def index(request):
    template = loader.get_template('index.html')
    context = {
        'redis_keys': [],
    }
    return HttpResponse(template.render(context, request))


def query_key(request):

    message = ""
    env_type = request.POST.get('envType')

    redis_nodes = []

    if env_type is not None:
        redis_nodes = constant.Const.redis_nodes_dict().get(env_type)
    else:
        return HttpResponseRedirect('/')

    redisconn = RedisCluster(startup_nodes=redis_nodes)

    param = request.POST.get('key')
    flag = request.POST.get('flag')

    list_keys = redisconn.keys("*" + param + "*")

    if flag == "0" and param is not None:
        for keys in list_keys:
            redisconn.delete(keys)
        message = "删除成功！"
        list_keys = ['']

    if flag == "1" and len(list_keys) == 0:
        message = "没有查询结果！"

    template = loader.get_template('index.html')
    context = {
        'redis_keys': list_keys,
        'key': param,
        'env_type':env_type,
        'message' : message
    }
    return HttpResponse(template.render(context, request))