# 使用 Playwright 官方提供的 Python Docker 镜像作为基础镜像
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# 设置工作目录为 /app
WORKDIR /app

# 复制 requirements.txt 并安装 Python 依赖
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 安装 Playwright 和 Chromium
RUN playwright install chromium

# 复制您的 Flask API 代码
COPY . .

# 暴露 API 端口（根据您的 Flask API 配置）
EXPOSE 5000

# 设置 IPC 模式为 host，优化性能
CMD ["python", "app.py", "--ipc=host"]
