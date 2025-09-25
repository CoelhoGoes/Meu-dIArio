from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à minha API FastAPI"}

@app.get("/saudacao/{nome}")
def read_item(nome: str):
    return {"saudacao": f"Olá, {nome}!"}

@app.post("/soma")
def somar(a: int, b: int):
    return {"resultado": a + b}