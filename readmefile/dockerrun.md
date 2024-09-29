你在 Docker Hub 上成功构建并推送了镜像后，可以通过以下步骤来使用该镜像：

### 1. 拉取镜像

首先，你需要从 Docker Hub 拉取镜像，可以选择不同的标签来拉取特定版本的镜像，例如 `latest` 或带有日期版本的镜像。

```sh
# 拉取最新版本的镜像
docker pull lihua/django-app:latest

# 拉取带有日期版本的镜像（例如20240929）
docker pull lihua/django-app:20240929
```

### 2. 运行镜像

拉取镜像后，你可以使用 `docker run` 命令运行容器。

```sh
# 运行最新版本的镜像
docker run -d -p 8000:8000 --name my-django-app lihua/django-app:latest
```

### 解释：

- **`docker run`**：用于运行一个新的容器。
- **`-d`**：以后台模式运行容器。
- **`-p 8000:8000`**：将容器的 8000 端口映射到宿主机的 8000 端口，这样你可以通过宿主机的 `http://localhost:8000` 来访问 Django 应用。
- **`--name my-django-app`**：为容器取一个名字 `my-django-app`。
- **`lihua/django-app:latest`**：指定你在 Docker Hub 上的镜像。

### 3. 访问应用

你运行容器后，Django 应用将会在 8000 端口启动，你可以在浏览器中访问：

```
http://localhost:8000
```

### 4. 停止和删除容器

如果需要停止容器，你可以使用以下命令：

```sh
# 停止容器
docker stop my-django-app

# 删除容器
docker rm my-django-app
```

### 5. 更新镜像

当你对代码进行更改并构建了新的镜像（例如使用 GitHub Actions 自动化流程），你可以通过以下步骤更新镜像：

1. **拉取新的镜像**：

   ```sh
   docker pull lihua/django-app:latest
   ```

2. **停止并删除旧容器**：

   ```sh
   docker stop my-django-app
   docker rm my-django-app
   ```

3. **运行新的容器**：

   ```sh
   docker run -d -p 8000:8000 --name my-django-app lihua/django-app:latest
   ```

这样，你就可以使用最新版本的 Django 应用了。



docker pull gwozai/django-app:latest
docker run -d -p 8001:8000 --name my-django-app lihua/django-app:latest
