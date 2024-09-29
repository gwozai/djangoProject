为了确保账号和密码的安全性，可以将它们都存储在 GitHub Secrets 中，并通过环境变量在 GitHub Actions 中使用。以下是更新后的 GitHub Actions 工作流文件：

### GitHub Actions Workflow 配置文件

1. 在 GitHub 项目中创建 `.github/workflows/docker-image.yml` 文件。
2. 将以下内容添加到该文件中：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main  # 当推送到 main 分支时触发构建
  pull_request:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      # 检出代码库
      - name: Checkout repository
        uses: actions/checkout@v2

      # 登录到 Docker Hub
      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      # 获取当前日期和最新版本号
      - name: Get current date and version
        id: version
        run: |
          DATE=$(date +'%Y%m%d')
          VERSION=$(git rev-parse --short HEAD)
          echo "DATE=$DATE" >> $GITHUB_ENV
          echo "VERSION=$VERSION" >> $GITHUB_ENV

      # 构建 Docker 镜像
      - name: Build Docker Image
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/django-app:latest \
                       -t ${{ secrets.DOCKER_USERNAME }}/django-app:${{ env.DATE }} \
                       -t ${{ secrets.DOCKER_USERNAME }}/django-app:${{ env.VERSION }} .

      # 推送 Docker 镜像到 Docker Hub
      - name: Push Docker Image
        run: |
          docker push ${{ secrets.DOCKER_USERNAME }}/django-app:latest
          docker push ${{ secrets.DOCKER_USERNAME }}/django-app:${{ env.DATE }}
          docker push ${{ secrets.DOCKER_USERNAME }}/django-app:${{ env.VERSION }}
```

### 主要修改：

1. **使用 GitHub Secrets 存储用户名和密码**
   - 将 Docker Hub 的用户名和密码分别存储为 GitHub Secrets，键名为 `DOCKER_USERNAME` 和 `DOCKER_PASSWORD`。

2. **使用环境变量**
   - 在 Docker Hub 登录步骤和镜像构建、推送步骤中，使用 `${{ secrets.DOCKER_USERNAME }}` 和 `${{ secrets.DOCKER_PASSWORD }}` 来引用用户名和密码。

### 设置 GitHub Secrets：

1. 打开你的 GitHub 仓库页面。
2. 进入 "Settings" -> "Secrets and variables" -> "Actions" -> "New repository secret"。
3. 添加两个新的 Secrets：
   - **Name**：`DOCKER_USERNAME`
     - **Value**：你的 Docker Hub 用户名（`lihua`）
   - **Name**：`DOCKER_PASSWORD`
     - **Value**：你的 Docker Hub 密码（`123456`）

这样，GitHub Actions 工作流就可以安全地使用 Docker Hub 的账号和密码来登录，并且不会在代码中暴露凭据。