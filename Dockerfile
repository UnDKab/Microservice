# Stage 1: Builder
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY app ./app

# Установка flask как глобального пакета
RUN pip install flask==2.2.3

# Проверка наличия flask в $PATH
RUN echo $PATH

ENV PATH="/usr/local/bin:$PATH"  
ENV FLASK_APP=app.main
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

