要创建一个完整的 Django ToDo 应用，以下是详细的步骤，包括项目结构、模型、视图、表单、模板和基本功能。这个简单的 ToDo 系统将允许你添加、查看、编辑和删除任务。

### 1. **创建 Django 项目和应用**

首先，确保你已经安装了 Django。如果还没有安装，请先运行以下命令：

```bash
pip install django
```

接着，创建 Django 项目和应用：

```bash
django-admin startproject todo_project
cd todo_project
python manage.py startapp tasks
```

### 2. **项目目录结构**

现在，你的项目目录应类似于这样：

```
todo_project/
│
├── manage.py
├── todo_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── tasks/
    ├── migrations/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
```

### 3. **配置 `settings.py`**

在项目的 `settings.py` 文件中，确保添加 `tasks` 应用到 `INSTALLED_APPS` 中：

```python
INSTALLED_APPS = [
    # Django 内置的应用
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 自定义应用
    'tasks',
]
```

### 4. **创建 `Task` 模型**

接下来，在 `tasks/models.py` 中定义任务的模型：

```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

### 5. **创建和应用数据库迁移**

运行以下命令以创建并应用数据库迁移，生成表格：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. **创建表单**

在 `tasks` 目录中创建一个 `forms.py` 文件，定义一个简单的表单，用于添加和编辑任务：

```python
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
```

### 7. **创建视图**

在 `tasks/views.py` 中，编写视图函数，处理任务的列表、添加、编辑和删除：

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
```

### 8. **配置 URL**

在 `tasks` 应用下创建一个 `urls.py` 文件，并添加以下代码来定义路由：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_add, name='task_add'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
]
```

同时，在 `todo_project/urls.py` 中，包含 `tasks` 应用的 URL 路由：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]
```

### 9. **创建模板**

在 `tasks` 应用下创建一个 `templates/tasks/` 目录，放置 HTML 模板文件。

#### `task_list.html` - 任务列表：

```html
<!DOCTYPE html>
<html>
<head>
    <title>ToDo List</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<div class="container">
    <h1>ToDo List</h1>
    <a href="{% url 'task_add' %}" class="btn btn-primary">Add Task</a>
    <table class="table">
        <thead>
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Completed</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for task in tasks %}
            <tr>
                <td>{{ task.title }}</td>
                <td>{{ task.description }}</td>
                <td>{{ task.completed }}</td>
                <td>
                    <a href="{% url 'task_edit' task.pk %}" class="btn btn-warning btn-sm">Edit</a>
                    <a href="{% url 'task_delete' task.pk %}" class="btn btn-danger btn-sm">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
</body>
</html>
```

#### `task_form.html` - 任务表单：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Task Form</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<div class="container">
    <h1>{{ form.instance.pk|yesno:"Edit Task,Add Task" }}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-success">Save</button>
        <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
    </form>
</div>
</body>
</html>
```

#### `task_confirm_delete.html` - 删除确认页面：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Delete Task</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<div class="container">
    <h1>Delete Task</h1>
    <p>Are you sure you want to delete "{{ task.title }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Delete</button>
        <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
    </form>
</div>
</body>
</html>
```

### 10. **启动开发服务器**

运行以下命令启动 Django 开发服务器：

```bash
python manage.py runserver
```

打开浏览器，访问 `http://127.0.0.1:8000/`，你将看到你的 ToDo 应用。你可以添加、编辑和删除任务。

### 11. **完成项目**

现在，你已经完成了一个基本的 Django ToDo 应用。你可以根据需要扩展它，比如添加用户身份验证、任务分类、优先级等功能。

这个实例是一个简化版的 ToDo 应用，但它涵盖了 Django 的基本功能，包括模型、视图、表单、模板和URL配置。







报错：
Internal Server Error: /
Traceback (most recent call last):
  File "C:\Users\58425\AppData\Local\Programs\Python\Python310\lib\site-packages\django\core\handlers\exception.py", line 55, in inner
    response = get_response(request)
  File "C:\Users\58425\AppData\Local\Programs\Python\Python310\lib\site-packages\django\core\handlers\base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "C:\Users\58425\PycharmProjects\djangoProject\tasks\views.py", line 10, in task_list
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
  File "C:\Users\58425\AppData\Local\Programs\Python\Python310\lib\site-packages\django\shortcuts.py", line 25, in render
  File "C:\Users\58425\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\loader.py", line 61, in render_to_string
    template = get_template(template_name, using=using)
  File "C:\Users\58425\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\loader.py", line 19, in get_template
    raise TemplateDoesNotExist(template_name, chain=chain)
django.template.exceptions.TemplateDoesNotExist: tasks/task_list.html

这个错误提示 `TemplateDoesNotExist: tasks/task_list.html`，表明 Django 没有找到 `tasks/task_list.html` 这个模板文件。通常，这是因为模板文件的路径不正确。

### 解决方案：

1. **检查模板文件的路径**  
   确保你的 `task_list.html` 文件在正确的位置。它应该位于 `tasks` 应用的 `templates/tasks/` 目录下，路径应类似于：

   ```
   tasks/
   ├── templates/
   │   └── tasks/
   │       └── task_list.html
   ```

   请确认模板目录的结构和文件是否存在。如果 `task_list.html` 文件不在正确的位置，请将它移动到 `tasks/templates/tasks/` 文件夹中。

2. **检查 `settings.py` 的模板设置**  
   确保 `settings.py` 中 `TEMPLATES` 的配置正确。在 `DIRS` 中可以添加全局模板路径：

   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [BASE_DIR / "templates"],  # 如果你有全局模板文件夹
           'APP_DIRS': True,  # 让 Django 自动在每个应用的 templates 目录中查找模板
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   ```

   上面的配置确保 Django 能够在 `tasks/templates/tasks/` 文件夹下找到模板文件。

3. **清理缓存或重启开发服务器**  
   有时 Django 可能缓存了错误的模板路径。如果你确认模板路径正确，尝试清理缓存或重启开发服务器：

   ```bash
   python manage.py runserver
   ```

4. **调试提示**  
   如果问题仍然存在，你可以添加一些调试代码，比如在 `views.py` 中打印 `BASE_DIR`，以确保你引用的模板路径正确：

   ```python
   from django.conf import settings
   import os
   
   print(os.path.join(settings.BASE_DIR, 'tasks/templates/tasks/task_list.html'))
   ```

这会帮助你确保 Django 正在查找的路径和你期望的一致。


## 
~~~bash
python manage.py startapp redis_app

~~~