from django.shortcuts import render
# redis_app/views.py

import redis
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
# redis_app/views.py

import redis
from django.conf import settings
from django.http import JsonResponse

# 获取 Redis 连接
def get_redis_connection():
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

# Redis 连接测试视图
def redis_test(request):
    try:
        conn = get_redis_connection()
        conn.ping()  # 测试连接是否成功
        return JsonResponse({"status": "success", "message": "Connected to Redis successfully."})
    except redis.ConnectionError as e:
        return JsonResponse({"status": "error", "message": str(e)})

# Redis 数据管理视图 (简单的设置和获取键值对)
def redis_manage(request):
    conn = get_redis_connection()
    action = request.GET.get('action', None)
    key = request.GET.get('key', None)
    value = request.GET.get('value', None)

    if action == 'set' and key and value:
        conn.set(key, value)
        return JsonResponse({"status": "success", "message": f"Key '{key}' set to '{value}'."})
    elif action == 'get' and key:
        value = conn.get(key)
        if value:
            return JsonResponse({"status": "success", "key": key, "value": value.decode()})
        else:
            return JsonResponse({"status": "error", "message": f"Key '{key}' not found."})
    else:
        return JsonResponse({"status": "error", "message": "Invalid parameters."})
def redis_home(request):
    return render(request, 'redis_app/index.html')

def redis_queue(request):
    return render(request, 'redis_app/queue.html')
# 获取队列信息视图
def redis_queue_info(request):
    conn = get_redis_connection()
    queue_name = request.GET.get('queue', 'default_queue')

    try:
        queue_length = conn.llen(queue_name)
        queue_items = conn.lrange(queue_name, 0, -1)
        queue_items = [item.decode() for item in queue_items]

        data = {
            'status': 'success',
            'queue_name': queue_name,
            'queue_length': queue_length,
            'queue_items': queue_items,
        }
    except redis.RedisError as e:
        data = {'status': 'error', 'message': str(e)}

    return JsonResponse(data)





# 向队列发送消息视图
@csrf_exempt  # 允许跨站请求，方便测试时使用
def send_message(request):
    if request.method == 'POST':
        conn = get_redis_connection()
        queue_name = request.POST.get('queue', 'default_queue')
        message = request.POST.get('message', '')

        if not message:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty.'})

        try:
            conn.rpush(queue_name, message)
            return JsonResponse({'status': 'success', 'message': f'Message "{message}" added to queue "{queue_name}".'})
        except redis.RedisError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
