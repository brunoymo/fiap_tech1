"""
Endpoint para dados de comercialização.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.utils.csv_downloader import CSVDownloader
from src.utils.filter_parser import parse_filters
import os
import logging

router = APIRouter(prefix="/comercializacao", tags=["Comercialização"])

# Inicializa o downloader de CSV
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
# Instanciar o CSVDownloader com o diretório /tmp
csv_downloader = CSVDownloader(data_dir="/tmp")

logger = logging.getLogger(__name__)

@router.get("/")
async def get_comercializacao(
    filtros: Dict[str, Any] = Depends(parse_filters)
) -> Dict[str, Any]:
    """
    Retorna dados de comercialização sem tipos específicos.
    """
    chave = "comercializacao"
    logger.info("Recebendo requisição para comercialização")
    try:
        dados = csv_downloader.get_data(chave)
        if not dados:
            logger.error("Dados não encontrados.")
            raise HTTPException(status_code=500, detail="Não foi possível obter dados.")
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
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")
