import sys
import os

# Proje kök dizinini Python yoluna ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import init_db, save_ticket, fetch_all_tickets
from services.ai_service import AISupportService
from core.models import SupportTicketRequest

def run_pipeline_simulation():
    # 1. Veritabanını başlat
    init_db()
    print("[INFO] SQLite Kurumsal Veritabanı Hazır.")

    # 2. Servisleri başlat
    ai_service = AISupportService()

    # 3. Farklı Telekom Senaryoları (VoIP, SMS, IP Santral)
    test_cases = [
        SupportTicketRequest(
            customer_id="CUST-9921",
            service_type="VoIP",
            issue_description="Müşteri VoIP aramalarında ses paketlerinin gitmediğini ve SIP register timeout hatası aldığını belirtiyor.",
            priority="High"
        ),
        SupportTicketRequest(
            customer_id="CUST-1045",
            service_type="SMS",
            issue_description="Toplu SMS gönderimlerinde SMPP gateway bağlantı reddi (Bind Failed) alınıyor.",
            priority="Critical"
        ),
        SupportTicketRequest(
            customer_id="CUST-3088",
            service_type="IP Santral",
            issue_description="Dahili 104 numaralı hat dış aramalara kapandı ve IVR menüsü döngüye giriyor.",
            priority="Medium"
        )
    ]

    print("\n" + "="*50)
    print(" CLOUDCELL ENTERPRISE AI SUPPORT PIPELINE - TEST KOŞUSU ")
    print("="*50)

    for idx, req in enumerate(test_cases, 1):
        print(f"\n[İŞLEM {idx}] Müşteri: {req.customer_id} | Servis: {req.service_type} | Öncelik: {req.priority}")
        
        # AI Analizi
        ai_result = ai_service.analyze_ticket(
            customer_id=req.customer_id,
            service_type=req.service_type,
            issue_description=req.issue_description,
            priority=req.priority
        )

        print(f" -> Teşhis: {ai_result['ai_diagnosis']}")
        print(f" -> Aksiyon: {ai_result['suggested_action']}")
        print(f" -> Durum : {ai_result['status']}")

        # Veritabanı Kaydı
        save_ticket(
            customer_id=req.customer_id,
            service_type=req.service_type,
            issue_description=req.issue_description,
            priority=req.priority,
            ai_diagnosis=ai_result['ai_diagnosis'],
            status=ai_result['status']
        )
        print(" -> [VERİTABANI] Bilet başarıyla arşivlendi.")

    # 4. Veritabanı Özet Raporunu Göster
    print("\n" + "="*50)
    print("--- VERİTABANI BİLET ÖZET RAPORU ---")
    print("="*50)
    tickets = fetch_all_tickets()
    print(f"{'ID':<5} | {'Müşteri':<10} | {'Servis':<12} | {'Öncelik':<10} | {'Durum':<22}")
    print("-" * 65)
    for t in tickets:
        # t formatı: (id, customer_id, service_type, priority, status, created_at)
        print(f"{t[0]:<5} | {t[1]:<10} | {t[2]:<12} | {t[3]:<10} | {t[4]:<22}")

    print("\n" + "="*50)
    print("[SUCCESS] Tüm kurumsal test senaryoları ve raporlama tamamlandı!")
    print("="*50)

if __name__ == "__main__":
    run_pipeline_simulation()