from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from services.auth import authenticate_user, create_access_token, verify_token, create_user
from models.auth import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


# --- Endpoints ---
@router.post("/register")
def register(user: RegisterRequest):
    try:
        user_id = create_user(user.name, user.email, user.password)
        return {"message": "Usuário criado com sucesso!", "user_id": user_id}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado: {str(e)}"
        )

@router.post("/login")
def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    access_token = create_access_token(data={"sub": str(user["id"])})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_current_user(token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    return {"email": token.get("sub")}
