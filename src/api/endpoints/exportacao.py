"""
Endpoint para dados de exportação.
"""
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import Dict, Any, Optional
from src.utils.csv_downloader import CSVDownloader
from src.utils.filter_parser import parse_filters
import os
from enum import Enum

router = APIRouter(prefix="/exportacao", tags=["Exportação"])

# Inicializa o downloader de CSV
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
# Instanciar o CSVDownloader com o diretório /tmp
csv_downloader = CSVDownloader(data_dir="/tmp")

class ExportacaoTipo(str, Enum):
    vinho = "vinho"
    espumante = "espumante"
    frescas = "frescas"
    suco = "suco"

@router.get("/{tipo}")
async def get_exportacao_tipo(
    tipo: ExportacaoTipo = Path(..., description="Tipo de exportação. Valores válidos: vinho, espumante, frescas, suco"),
    filtros: Dict[str, Any] = Depends(parse_filters)
) -> Dict[str, Any]:
    """
    Retorna dados de exportação de acordo com o tipo especificado.
    """
    tipos_validos = [
        "vinho", "espumante", "frescas", "suco"
    ]
    chave = f"exportacao_{tipo}"
    if tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo de exportação inválido. Tipos válidos: vinho, espumante, frescas, suco.")
    try:
        dados = csv_downloader.get_data(chave)
        if not dados:
            raise HTTPException(status_code=500, detail="Não foi possível obter dados de exportação.")
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
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados de exportação: {str(e)}")
