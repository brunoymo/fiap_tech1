"""
Endpoint para subcategorias de todas as categorias.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from src.utils.csv_downloader import CSVDownloader
import os
import logging

router = APIRouter(prefix="/subcategorias", tags=["Subcategorias"])

# Inicializa o downloader de CSV
csv_downloader = CSVDownloader(data_dir="/tmp")
logger = logging.getLogger(__name__)

@router.get("/{categoria}")
async def get_subcategorias_categoria(categoria: str):
    """
    Retorna dados de subcategorias para a categoria especificada.
    """
    try:
        if categoria not in csv_downloader.DOWNLOAD_URLS.keys():
            raise HTTPException(status_code=400, detail="Categoria inválida para subcategorias.")

        dados = csv_downloader.get_data(categoria)
        if not dados:
            raise HTTPException(status_code=500, detail="Não foi possível obter dados de subcategorias.")

        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados de subcategorias: {str(e)}")

@router.get("/{tipo}")
async def get_subcategorias_tipo(tipo: str):
    logger.info(f"Recebendo requisição para tipo: {tipo}")
    try:
        dados = csv_downloader.get_data(tipo)
        if not dados:
            logger.error("Dados não encontrados.")
            raise HTTPException(status_code=500, detail="Não foi possível obter dados de subcategorias.")
        return dados
    except Exception as e:
        logger.error(f"Erro ao processar dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")
