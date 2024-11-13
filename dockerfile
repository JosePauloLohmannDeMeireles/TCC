FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0 cmake build-essential pkg-config && \
    apt-get install -y libsm6 libxext6 libxrender-dev && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 5000

CMD ["python", "main.py"]
