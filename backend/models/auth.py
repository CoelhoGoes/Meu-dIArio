from pydantic import BaseModel

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

# --- Schemas auxiliares ---
class LoginRequest(BaseModel):
    email: str
    password: str