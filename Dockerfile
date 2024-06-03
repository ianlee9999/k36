# 使用官方 Python 映像
FROM python:3.8-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄的內容到容器的 /app 目錄
COPY . /app

# 安裝所需的 Python 庫
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 whois 工具
RUN apt-get update && apt-get install -y whois

# 暴露 Flask 默認端口
EXPOSE 6000

# 設置環境變量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 啟動 Flask 應用
CMD ["flask", "run"]
