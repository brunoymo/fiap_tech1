"""
Endpoint para dados de comercialização.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import Dict, Any, Optional
from src.utils.csv_downloader import CSVDownloader
from src.utils.filter_parser import parse_filters
import os
from enum import Enum
import logging

router = APIRouter(prefix="/comercializacao", tags=["Comercialização"])

# Inicializa o downloader de CSV
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
# Instanciar o CSVDownloader com o diretório /tmp
csv_downloader = CSVDownloader(data_dir="/tmp")

class ComercializacaoTipo(str, Enum):
    comercializacao = "comercializacao"

logger = logging.getLogger(__name__)

@router.get("/{tipo}")
async def get_comercializacao_tipo(
    tipo: ComercializacaoTipo = Path(..., description="Tipo de comercialização. Valores válidos: comercializacao"),
    filtros: Dict[str, Any] = Depends(parse_filters)
) -> Dict[str, Any]:
    """
    Retorna dados de comercialização de acordo com o tipo especificado.
    """
    logger.info(f"Recebendo requisição para tipo: {tipo}")
    tipos_validos = [
        "comercializacao"
    ]
    chave = f"{tipo}"
    if tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo de comercialização inválido. Tipos válidos: comercializacao.")
    try:
        dados = csv_downloader.get_data(chave)
        if not dados:
            logger.error("Dados não encontrados.")
            raise HTTPException(status_code=500, detail="Não foi possível obter dados de comercialização.")
        # Aplica filtros se fornecidos
        if filtros:
            dados_filtrados = []
            for item in dados["data"]:
                match = True
                for key, value in filtros.items():
                    if key in item and str(item[key]).lower() != str(value).lower():
                        match = False
                        break
                if match:
                    dados_filtrados.append(item)
            dados["data"] = dados_filtrados
        return dados
    except Exception as e:
        logger.error(f"Erro ao processar dados: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados de comercialização: {str(e)}")

@router.get("/{categoria}")
async def get_comercializacao_categoria(categoria: str):
    """
    Retorna dados de comercialização para a categoria especificada.
    """
    try:
        if categoria not in ["comercializacao"]:
            raise HTTPException(status_code=400, detail="Categoria inválida para comercialização.")

        dados = csv_downloader.get_data(categoria)
        if not dados:
            raise HTTPException(status_code=500, detail="Não foi possível obter dados de comercialização.")

        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados de comercialização: {str(e)}")
