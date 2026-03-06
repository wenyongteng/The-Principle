FROM python:3.10

WORKDIR /app

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

# 初始化空记忆
RUN touch consciousness.txt

EXPOSE 8000

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "8000"]
