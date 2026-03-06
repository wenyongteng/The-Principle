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

# 复制种子数据（首次启动时灌入持久化目录）
COPY seed_data/ ./seed_data/

# 复制入口脚本
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# 持久化数据目录
ENV DATA_DIR=/data
RUN mkdir -p /data

EXPOSE 8000

CMD ["./entrypoint.sh"]
