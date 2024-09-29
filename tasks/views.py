from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import redis

redis_client = redis.StrictRedis(host='1.15.7.2', port=6372, db=0)

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-priority')  # 按优先级排序，且只显示当前用户的任务
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # 不直接保存，等待设置 user
            task.user = request.user  # 将当前登录用户设置为任务的 user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # 确保当前用户只能编辑自己的任务
    if task.user != request.user:
        return redirect('task_list')

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # 确保当前用户只能删除自己的任务
    if task.user != request.user:
        return redirect('task_list')

    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)  # 自动登录

            # 添加注册成功的消息
            messages.success(request, f'Registration successful! Welcome, {username}.')

            return redirect('task_list')  # 注册成功后重定向到任务列表页面
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def producer_view(request):
    if request.method == "POST":
        message = request.POST.get('message', 'Default Message')
        redis_client.lpush('task_queue', message)  # 将消息放入 Redis 列表中

    # 获取当前 Redis 队列中的所有消息
    queue_messages = redis_client.lrange('task_queue', 0, -1)  # 获取队列中所有的消息

    # 将消息解码并传递到模板
    queue_messages = [msg.decode('utf-8') for msg in queue_messages]

    return render(request, 'producer.html', {'queue_messages': queue_messages})