from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False, verbose_name='Task Completed')  # 任务是否完成
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')  # 任务优先级
    due_date = models.DateTimeField(default=timezone.now, blank=True, null=True)  # 任务截止日期
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # 分类

    def __str__(self):
        return self.title
