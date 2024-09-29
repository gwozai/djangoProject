要创建一个只包含 Django 项目的 Docker 镜像，可以使用一个简化版本的 `Dockerfile`，其中只打包 Django Web 应用，而不依赖 `docker-compose` 的 Redis 服务。以下是完整的步骤：

### 1. 创建新的 Dockerfile

在 Django 项目的根目录下创建一个名为 `Dockerfile` 的文件。该文件描述了如何构建只包含 Django Web 应用的 Docker 镜像。

#### 新的 `Dockerfile`

```dockerfile
# 使用官方的 Python 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制 Django 项目代码到工作目录
COPY . /app/

# 环境变量设置，防止 Python 生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE 1
# 环境变量设置，确保 Python 日志立即输出
ENV PYTHONUNBUFFERED 1

# 暴露应用运行端口
EXPOSE 8000

# 运行 Django 应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 2. 修改 Redis 配置（如果需要）

如果要让这个镜像独立于 `docker-compose` 运行，你可以在 `settings.py` 中将 Redis 主机地址改为你期望的值。例如，连接到一个远程 Redis 服务器：

```python
# settings.py

REDIS_HOST = 'your-redis-server-ip'  # 远程 Redis 服务的 IP 地址
REDIS_PORT = 6379
REDIS_DB = 0
```

如果不使用 Redis，可以注释或删除相关的 Redis 配置。

### 3. 构建新的 Docker 镜像

使用以下命令来构建 Docker 镜像。在项目的根目录下执行：

```bash
docker build -t django_web_app .
```

这里 `-t django_web_app` 是镜像的标签名称，你可以根据需要更改它。

### 4. 运行新的 Docker 镜像

构建完成后，可以使用以下命令运行 Docker 镜像：

```bash
docker run -d -p 8000:8000 --name django_web_app_container django_web_app
```

- `-d`：以后台模式运行容器。
- `-p 8000:8000`：将容器的 8000 端口映射到主机的 8000 端口。
- `--name django_web_app_container`：给容器指定一个名称。
- `django_web_app`：这是前面构建的镜像名称。

### 5. 访问应用程序

现在你的 Django 应用程序在 Docker 中运行，并且通过 `http://localhost:8000` 访问。

### 6. 停止和删除容器

如果你需要停止和删除正在运行的容器，可以使用以下命令：

```bash
docker stop django_web_app_container
docker rm django_web_app_container
```

这样你就成功地创建了一个只包含 Django Web 应用的 Docker 镜像，并通过它来运行你的 Django 项目。这个镜像与 Redis 服务解耦，可以独立运行或者连接到你配置的远程 Redis 服务。