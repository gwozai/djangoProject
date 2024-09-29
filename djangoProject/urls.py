from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),  # 包含你的 tasks 应用的 URL

    # 添加登录和注销的 URL
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redis/', include('redis_app.urls')),  # 包含 Redis 的 URL 路由

]
