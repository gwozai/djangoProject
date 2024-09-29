from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # 注册 URL

    path('', views.task_list, name='task_list'),
    path('add/', views.task_add, name='task_add'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('producer/', views.producer_view, name='producer'),

]