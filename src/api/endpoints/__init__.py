"""
Módulo de inicialização para endpoints.
"""
from fastapi import APIRouter
from src.api.endpoints import producao, processamento, comercializacao, importacao, exportacao, subcategorias

# Criação do router principal
router = APIRouter(prefix="/api/v1")

# Inclusão dos routers de cada endpoint
router.include_router(producao.router, prefix="/producao")
router.include_router(processamento.router, prefix="/processamento")
router.include_router(comercializacao.router, prefix="/comercializacao")
router.include_router(importacao.router, prefix="/importacao")
router.include_router(exportacao.router, prefix="/exportacao")
router.include_router(subcategorias.router, prefix="/subcategorias")

__all__ = ['router']
