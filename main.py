
import os
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Minha API")

class NovaTarefa(BaseModel):
    titulo: str

def conectar():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL não configurada")
    return psycopg.connect(url, connect_timeout=10)

@app.get("/")
def inicio():
    return {"mensagem": "Minha API Python está funcionando!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tarefas")
def listar_tarefas():
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, titulo FROM tarefas ORDER BY id"
                )
                linhas = cur.fetchall()
                return [
                    {"id": linha[0], "titulo": linha[1]}
                    for linha in linhas
                ]
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao consultar tarefas: {erro}"
        )

@app.post("/tarefas")
def criar_tarefa(tarefa: NovaTarefa):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tarefas (titulo) VALUES (%s) RETURNING id, titulo",
                    (tarefa.titulo,)
                )
                linha = cur.fetchone()
                return {"id": linha[0], "titulo": linha[1]}
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar tarefa: {erro}"
        )
