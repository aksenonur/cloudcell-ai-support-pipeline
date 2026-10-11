from fastapi import FastAPI, HTTPException
import sys
import os

# Proje kök dizinini Python yoluna ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from core.models import SupportTicketRequest
from services.ai_service import AISupportService
from db.database import init_db, save_ticket, fetch_all_tickets

app = FastAPI(
    title="CloudCell Enterprise AI Support API",
    description="Telekomünikasyon altyapısı için AI destekli arıza teşhis ve biletleme servisi",
    version="1.0.0"
)

# Uygulama ayağa kalkarken veritabanını hazırla
@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/api/v1/analyze-ticket")
def analyze_and_save_ticket(ticket: SupportTicketRequest):
    """
    Dış sistemlerden gelen bilet isteklerini alır, AI ile analiz eder ve veritabanına kaydeder.
    """
    try:
        ai_service = AISupportService()
        
        # AI Analizi çalıştır
        ai_result = ai_service.analyze_ticket(
            customer_id=ticket.customer_id,
            service_type=ticket.service_type,
            issue_description=ticket.issue_description,
            priority=ticket.priority
        )

        # Veritabanına kaydet
        save_ticket(
            customer_id=ticket.customer_id,
            service_type=ticket.service_type,
            issue_description=ticket.issue_description,
            priority=ticket.priority,
            ai_diagnosis=ai_result['ai_diagnosis'],
            status=ai_result['status']
        )

        return {
            "status": "success",
            "message": "Bilet başarıyla analiz edildi ve arşivlendi.",
            "data": {
                "customer_id": ticket.customer_id,
                "service_type": ticket.service_type,
                "diagnosis": ai_result['ai_diagnosis'],
                "suggested_action": ai_result['suggested_action'],
                "ticket_status": ai_result['status']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/tickets")
def get_all_tickets():
    """
    Sistemde kayıtlı tüm destek biletlerini listeler.
    """
    try:
        rows = fetch_all_tickets()
        tickets = []
        for r in rows:
            tickets.append({
                "id": r[0],
                "customer_id": r[1],
                "service_type": r[2],
                "priority": r[3],
                "status": r[4],
                "created_at": r[5]
            })
        return {"status": "success", "count": len(tickets), "tickets": tickets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))