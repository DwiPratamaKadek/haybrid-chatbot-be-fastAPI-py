from google import genai
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

class GeminiService:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # Model utama + fallback
        self.models = [
            "gemini-2.5-flash",
            "gemini-1.5-flash"
        ]

    def generate(self, prompt: str, max_retries: int = 5) -> str:
        """
        Generate response dari Gemini dengan:
        - Retry + exponential backoff
        - Fallback model
        - Error handling
        """

        for model_name in self.models:
            logging.info(f"🔹 Mencoba model: {model_name}")

            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )

                    return self._extract_text(response)

                except Exception as e:
                    wait_time = min(2 ** attempt, 30)

                    logging.warning(
                        f"[{model_name}] Retry {attempt+1}/{max_retries} gagal: {e}"
                    )

                    # Kalau sudah retry terakhir → pindah model
                    if attempt == max_retries - 1:
                        logging.error(f"❌ Model {model_name} gagal total")
                        break

                    time.sleep(wait_time)

        # Kalau semua model gagal
        return self._fallback_response()

    def _extract_text(self, response) -> str:
        """
        Ekstrak teks dari response Gemini dengan aman
        """
        try:
            if not response.candidates:
                return "Maaf, model tidak memberikan respon."

            return response.candidates[0].content.parts[0].text

        except Exception as e:
            logging.error(f"Error parsing response: {e}")
            return "Terjadi kesalahan saat memproses respon model."

    def _fallback_response(self) -> str:
        """
        Response jika semua model gagal
        """
        return (
            "Maaf, sistem sedang mengalami gangguan atau beban tinggi. "
            "Silakan coba kembali dalam beberapa saat."
        )
