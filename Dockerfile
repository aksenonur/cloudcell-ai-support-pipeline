# Resmi hafif Python imajını temel al
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını güncelle ve gerekli araçları kur
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılık dosyasını kopyala ve pip'i güncelle
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Proje kaynak kodlarını çalışma dizinine kopyala
COPY . .

# Konteynerin dışarıya açacağı port
EXPOSE 8000

# FastAPI uygulamasını Uvicorn sunucusu ile başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]