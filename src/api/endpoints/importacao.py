"""
Endpoint para dados de importação.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import Dict, Any, Optional
from src.utils.csv_downloader import CSVDownloader
from src.utils.filter_parser import parse_filters
import os
from enum import Enum
import logging

router = APIRouter(prefix="/importacao", tags=["Importação"])

# Inicializa o downloader de CSV
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
# Instanciar o CSVDownloader com o diretório /tmp
csv_downloader = CSVDownloader(data_dir="/tmp")

class ImportacaoTipo(str, Enum):
    vinho = "vinho"
    espumante = "espumante"
    frescas = "frescas"
    passas = "passas"
    suco = "suco"

logger = logging.getLogger(__name__)

@router.get("/{tipo}")
async def get_tipo(
    tipo: str = Path(..., description="Tipo de dado. Valores válidos: vinho, espumante, frescas, passas, suco"),
    filtros: Dict[str, Any] = Depends(parse_filters)
) -> Dict[str, Any]:
    """
    Retorna dados de acordo com o tipo especificado.
    """
    tipos_validos = ["vinho", "espumante", "frescas", "passas", "suco"]
    chave = f"importacao_{tipo}"
    if tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo inválido. Tipos válidos: vinho, espumante, frescas, passas, suco.")
    logger.info(f"Recebendo requisição para tipo: {tipo}")
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
