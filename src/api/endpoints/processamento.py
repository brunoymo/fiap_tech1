"""
Endpoint para dados de processamento.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import Dict, Any, Optional
from src.utils.csv_downloader import CSVDownloader
from src.utils.filter_parser import parse_filters
import os
from enum import Enum

router = APIRouter(prefix="/processamento", tags=["Processamento"])

# Inicializa o downloader de CSV
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
# Instanciar o CSVDownloader com o diretório /tmp
csv_downloader = CSVDownloader(data_dir="/tmp")

class ProcessamentoTipo(str, Enum):
    viniferas = "viniferas"
    americanas = "americanas"
    mesa = "mesa"

@router.get("/{tipo}")
async def get_processamento_tipo(
    tipo: ProcessamentoTipo = Path(..., description="Tipo de processamento. Valores válidos: viniferas, americanas, mesa"),
    filtros: Dict[str, Any] = Depends(parse_filters)
) -> Dict[str, Any]:
    """
    Retorna dados de processamento de acordo com o tipo especificado.
    """
    tipos_validos = [
        "viniferas", "americanas", "mesa"
    ]
    chave = f"processamento_{tipo}"
    if tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo de processamento inválido. Tipos válidos: viniferas, americanas, mesa.")
    try:
        dados = csv_downloader.get_data(chave)
        if not dados:
            raise HTTPException(status_code=500, detail="Não foi possível obter dados de processamento.")
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
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados de processamento: {str(e)}")
