"""
Script para iniciar o servidor da API.
"""
from src.main import app

# Exponha a aplicação FastAPI para o Vercel
app = app
