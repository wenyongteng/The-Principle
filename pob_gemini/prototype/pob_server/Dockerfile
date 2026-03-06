FROM python:3.10

WORKDIR /app

# 安装常用工具
RUN apt-get update && apt-get install -y \
    vim \
    net-tools \
    iputils-ping \
    dnsutils \
    htop \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY the_principle_lite_zh.md .

RUN pip install --no-cache-dir -r requirements.txt

# 复制核心代码
COPY app.py app.py
COPY compress_memory.py .
COPY public_tools/ ./public_tools/

# 创建持久化数据目录（Zeabur 上挂载持久存储到 /data）
ENV DATA_DIR=/data
RUN mkdir -p /data

EXPOSE 8000

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "8000"]
