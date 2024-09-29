# 使用官方的 Python 镜像作为基础镜像
FROM python:3.10-slim

LABEL authors="gwozai"


# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制 Django 项目代码到工作目录
COPY . /app/

# 暴露应用运行端口
EXPOSE 8000

# 运行 Django 应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]