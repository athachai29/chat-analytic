from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    fastapi_title: str
    fastapi_description: str
    fastapi_contact_name: str
    fastapi_contact_url: str
    fastapi_contact_email: EmailStr
    fastapi_license_info_name: str
    fastapi_license_info_url: str
    db_url: str

    class Config:
        env_file = ".env"
