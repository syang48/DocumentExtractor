FROM python:3.10-slim
# Install LibreOffice and Fonts
RUN apt-get update && apt-get install -y \
    libreoffice-writer fonts-liberation --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
# Start your app
CMD ["python", "main.py"]