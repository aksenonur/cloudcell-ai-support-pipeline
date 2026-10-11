from pydantic import BaseModel, Field

class SupportTicketRequest(BaseModel):
    customer_id: str = Field(..., description="Müşteri ID'si")
    service_type: str = Field(..., description="Hizmet türü (örn. VoIP, SMS, IP Santral)")
    issue_description: str = Field(..., description="Yaşanan teknik sorunun detaylı açıklaması")
    priority: str = Field(default="Medium", description="Öncelik seviyesi (High, Medium, Low)")