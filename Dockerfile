FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libreoffice-writer \
    fonts-liberation \
    default-jre-headless \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
