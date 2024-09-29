# redis_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.redis_home, name='redis_home'),  # 主页面
    path('queue/', views.redis_queue, name='redis_queue'),  # 主页面

    path('test/', views.redis_test, name='redis_test'),
    path('manage/', views.redis_manage, name='redis_manage'),
    path('queue_info/', views.redis_queue_info, name='redis_queue_info'),  # 获取队列信息
    path('send_message/', views.send_message, name='send_message'),  # 发送消息到队列

]
