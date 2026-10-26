
from fastapi import FastAPI

app = FastAPI(title="Minha API")

@app.get("/")
def inicio():
    return {
        "mensagem": "Minha API Python está funcionando!"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

