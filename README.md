# CloudCell Enterprise AI Support Pipeline

CloudCell Telekomünikasyon A.Ş. için geliştirilmiş; VoIP, SMS (SMPP) ve IP Santral altyapılarında yaşanan teknik arızaları yapay zeka ile otomatik teşhis eden ve çözüm aksiyonu üreten kurumsal destek boru hattı (pipeline).

## Öne Çıkan Özellikler

- **Çoklu Telekom Desteği:** VoIP (SIP/Codec), SMS (SMPP Gateway) ve IP Santral sorunları için özelleştirilmiş AI analiz motoru.
- **Fail-Safe & Fallback Mimarisi:** OpenAI API anahtarı veya bağlantısı olmasa dahi kesintisiz çalışmayı sürdüren akıllı telekom simülasyon motoru.
- **Veri Doğrulama (Pydantic):** Gelen bilet verilerini tipe ve formata göre sıkı denetimden geçiren katman.
- **Kalıcı Depolama (SQLite):** İşlenen tüm analizlerin, teşhislerin ve aksiyon planlarının ilişkisel veritabanı arşivlenmesi.
- **Raporlama & CLI İzleme:** Veritabanındaki aktif bilet durumlarını anlık olarak konsola raporlama yeteneği.

##  Proje Mimarisi
cloudcell-ai-support-pipeline/
│
├── config/             # Yapılandırma ve çevre değişkenleri (.env)
├── core/               # Pydantic veri modelleri ve iş kuralları (models.py)
├── db/                 # SQLite veritabanı yönetimi ve CRUD (database.py)
├── services/           # OpenAI & Fallback AI analiz servisleri (ai_service.py)
├── utils/              # Kurumsal loglama ve yardımcı araçlar (logger.py)
├── logs/               # Sistem log kayıtları (cloudcell_pipeline.log)
├── main.py             # Pipeline simülasyon ve orkestrasyon dosyası
└── cloudcell_support.db # SQLite veritabanı dosyası

## Kurulum ve Çalıştırma

1. Sanal ortamı aktifleştirin:
   ```powershell
   .\venv\Scripts\activate
