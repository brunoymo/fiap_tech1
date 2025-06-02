"""
Aplicação principal da API de Vitivinicultura da Embrapa.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.api.endpoints import router
from src.utils.config import API_TITLE, API_DESCRIPTION, API_VERSION

# Criação da aplicação FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS para permitir acesso de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas
app.include_router(router)

# Rota raiz
@app.get("/", tags=["root"])
async def root():
    """
    Rota raiz da API, retorna informações básicas.
    """
    return {
        "api": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": [
            "/api/v1/producao",
            "/api/v1/processamento",
            "/api/v1/comercializacao",
            "/api/v1/importacao",
            "/api/v1/exportacao",
            "/api/v1/subcategorias",
        ]
    }

# Personalização da documentação OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    
    # Personalização adicional do esquema OpenAPI
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.embrapa.br/tema/embrapa-portal/portal_assets/images/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
