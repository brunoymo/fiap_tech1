"""
Script para iniciar o servidor da API.
"""
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "API funcionando!"}

@app.get("/teste")
async def teste():
    return {"message": "Rota de teste funcionando!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
