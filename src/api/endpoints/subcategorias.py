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
async def get_subcategorias(categoria: str) -> Dict[str, Any]:
    """
    Retorna as subcategorias disponíveis para filtragem na categoria especificada.
    
    Args:
        categoria: Nome da categoria (producao, processamento, comercializacao, importacao, exportacao)
    """
    categorias_validas = ["producao", "processamento", "comercializacao", "importacao", "exportacao"]
    
    if categoria not in categorias_validas:
        raise HTTPException(
            status_code=400,
            detail=f"Categoria inválida. Categorias válidas: {', '.join(categorias_validas)}"
        )
    
    logger.info(f"Recebendo requisição para categoria: {categoria}")
    try:
        dados = csv_downloader.get_data(categoria)
        
        if not dados:
            logger.error(f"Dados não encontrados para a categoria: {categoria}")
            raise HTTPException(
                status_code=500, 
                detail=f"Não foi possível obter subcategorias de {categoria}. Tente novamente mais tarde."
            )
        
        logger.info(f"Dados obtidos com sucesso para a categoria: {categoria}")
        return {
            "categoria": categoria,
            "subcategorias": dados["subcategorias"]
        }
    
    except Exception as e:
        logger.error(f"Erro ao obter subcategorias de {categoria}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter subcategorias de {categoria}: {str(e)}"
        )

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
