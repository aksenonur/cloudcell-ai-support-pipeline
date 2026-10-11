import pytest
from core.models import SupportTicketRequest
from services.ai_service import AISupportService

def test_ticket_request_model():
    """Pydantic model doğrulamasını test eder."""
    req = SupportTicketRequest(
        customer_id="TEST-123",
        service_type="VoIP",
        issue_description="Test arızası",
        priority="High"
    )
    assert req.customer_id == "TEST-123"
    assert req.service_type == "VoIP"

def test_ai_fallback_diagnosis():
    """OpenAI API anahtarı yokken Fallback simülasyonunun doğru çalıştığını test eder."""
    ai_service = AISupportService()
    result = ai_service.analyze_ticket(
        customer_id="TEST-123",
        service_type="VoIP",
        issue_description="SIP register timeout hatası alınıyor.",
        priority="High"
    )
    assert "ai_diagnosis" in result
    assert "suggested_action" in result
    assert result["status"] == "In Progress (Simulated)"