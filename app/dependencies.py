from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from .config import API_KEY
from .config import API_KEY_NAME

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")
    return True