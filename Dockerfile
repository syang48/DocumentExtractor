FROM python:3.10-slim

# 1. Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer \
    libreoffice-java-common \
    default-jre-headless \
    fonts-liberation \
    libgl1 \
    libglib2.0-0 \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 2. VERIFY and LINK
# This ensures that if it's installed, it's definitely in /usr/bin/soffice
RUN ln -s /usr/lib/libreoffice/program/soffice /usr/bin/soffice || true \
    && soffice --version # If this fails, the build stops here.

# 3. Environment & Workspace
ENV HOME=/tmp
WORKDIR /app

# 4. App Setup
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Ensure storage exists and is writable by any user
RUN mkdir -p storage/uploads storage/output && chmod -R 777 storage

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]