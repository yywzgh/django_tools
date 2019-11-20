from django.http import HttpResponse
from django.template import loader
from rediscluster import RedisCluster


def index(request):
    template = loader.get_template('index.html')
    context = {
        'redis_keys': [],
    }
    return HttpResponse(template.render(context, request))


def query_key(request):

    message = ""

    redis_nodes = [{'host': '10.25.16.253', 'port': 9701},
                   {'host': '10.25.16.253', 'port': 9702},
                   {'host': '10.25.16.253', 'port': 9703},
                   {'host': '10.25.16.253', 'port': 9704},
                   {'host': '10.25.16.253', 'port': 9705},
                   {'host': '10.25.16.253', 'port': 9706}
                   ]

    redisconn = RedisCluster(startup_nodes=redis_nodes)

    param = request.POST['key']
    flag = request.POST['flag']

    list_keys = redisconn.keys("*" + param + "*")

    if flag == "0" and param != "":
        for keys in list_keys:
            redisconn.delete(keys)
            message = "删除成功！"
            list_keys = ['']

    template = loader.get_template('index.html')
    context = {
        'redis_keys': list_keys,
        'key': param,
        'message' : message
    }
    return HttpResponse(template.render(context, request))