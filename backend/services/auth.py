from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError 
import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from connections.postgres import PostgresConnection
from dotenv import load_dotenv
import os

load_dotenv()

# Config JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# --- Interações com banco ---
def get_user_by_email(email: str):
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cur.fetchone()
    finally:
        conn.close()


def create_user(name: str, email: str, password: str):
    conn = PostgresConnection().get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # 1. Verifica se já existe um usuário com o mesmo email
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            if existing_user:
                raise ValueError("E-mail já cadastrado")

            # 2. Gera o hash da senha
            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            # 3. Insere o usuário novo
            cur.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                (name, email, password_hash)
            )
            user_id = cur.fetchone()["id"]
            conn.commit()
            return user_id
    finally:
        conn.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# --- Lógica de autenticação ---
def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return {"user_id": user_id}
    except (JWTError, Exception):
        return None
