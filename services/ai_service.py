import os
import openai
from dotenv import load_dotenv

load_dotenv()

class AISupportService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def analyze_ticket(self, customer_id: str, service_type: str, issue_description: str, priority: str) -> dict:
        """Destek biletini OpenAI ile analiz eder; API anahtarı yoksa akıllı simülasyon moduna geçer."""
        if not self.client:
            return self._simulate_ai_response(service_type, issue_description)
        
        try:
            prompt = (
                f"Sen CloudCell Telekomünikasyon A.Ş. uzman AI teknik destek asistanısın.\n"
                f"Servis Türü: {service_type}\n"
                f"Öncelik: {priority}\n"
                f"Sorun Açıklaması: {issue_description}\n\n"
                f"Lütfen bu sorun için teknik teşhis ve çözüm önerisi üret."
            )
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            ai_text = response.choices[0].message.content
            return {
                "ai_diagnosis": ai_text,
                "suggested_action": "Gerçek OpenAI Modeli ile Çözüm Sağlandı",
                "status": "In Progress"
            }
        except Exception as e:
            return self._simulate_ai_response(service_type, issue_description)

    def _simulate_ai_response(self, service_type: str, issue_description: str) -> dict:
        """OpenAI API anahtarı olmadığında veya hata durumunda profesyonel telekom simülasyonu çalıştırır."""
        if service_type == "VoIP":
            diagnosis = "SIP register timeout veya codec uyumsuzluğu tespit edildi."
            action = "NAT keep-alive ayarlarını kontrol edin ve SBC rotalarını doğrulayın."
        elif service_type == "SMS":
            diagnosis = "SMPP gateway bağlantı reddi veya rota (route) kısıtlaması."
            action = "IP Whitelist kontrolü yapın ve SMPP bind isteklerini yeniden yapılandırın."
        else:
            diagnosis = "Genel IP Santral / Altyapı uyarısı."
            action = "WAN/LAN switch port durumlarını ve hat sürekliliğini test edin."

        return {
            "ai_diagnosis": diagnosis,
            "suggested_action": action,
            "status": "In Progress (Simulated)"
        }