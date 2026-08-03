from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./andatest.db"
    secret_key: str = "dev-secret-key"
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:5500"]
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    asistente_limite_diario: int = 40
    # Emails con acceso al dashboard de administración (/admin.html). Sin
    # columna is_admin en Usuario a propósito, para no requerir migración.
    # str (no list[str]) porque pydantic-settings intenta JSON-decodear
    # cualquier campo list[str] leído del .env ANTES de nuestro validador, y
    # revienta si el valor no es JSON válido (p.ej. vacío o "a@b.com,c@d.com").
    admin_emails: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    @property
    def admin_emails_list(self) -> list[str]:
        return [e.strip().lower() for e in self.admin_emails.split(",") if e.strip()]


settings = Settings()
