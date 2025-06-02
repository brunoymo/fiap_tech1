"""
Endpoint para subcategorias de todas as categorias.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from src.utils.csv_downloader import CSVDownloader
import os

router = APIRouter(prefix="/subcategorias", tags=["Subcategorias"])

# Inicializa o downloader de CSV
csv_downloader = CSVDownloader(data_dir="/tmp")

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
    
    try:
        dados = csv_downloader.get_data(categoria)
        
        if not dados:
            raise HTTPException(
                status_code=500, 
                detail=f"Não foi possível obter subcategorias de {categoria}. Tente novamente mais tarde."
            )
        
        return {
            "categoria": categoria,
            "subcategorias": dados["subcategorias"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter subcategorias de {categoria}: {str(e)}"
        )
