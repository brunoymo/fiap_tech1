"""
Configurações globais para a API de Vitivinicultura da Embrapa.
"""
import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = os.path.join(BASE_DIR, "data")

# Configurações da API
API_TITLE = "API de Vitivinicultura da Embrapa"
API_DESCRIPTION = "API para consulta de dados de vitivinicultura da Embrapa, incluindo produção, processamento, comercialização, importação e exportação."
API_VERSION = "1.0.0"

# Configurações de requisições
REQUEST_TIMEOUT = 30  # segundos

# URLs base da Embrapa
EMBRAPA_BASE_URL = "http://vitibrasil.cnpuv.embrapa.br"
PRODUCAO_URL = f"{EMBRAPA_BASE_URL}/index.php?opcao=opt_01"
PROCESSAMENTO_URL = f"{EMBRAPA_BASE_URL}/index.php?opcao=opt_02"
COMERCIALIZACAO_URL = f"{EMBRAPA_BASE_URL}/index.php?opcao=opt_03"
IMPORTACAO_URL = f"{EMBRAPA_BASE_URL}/index.php?opcao=opt_04"
EXPORTACAO_URL = f"{EMBRAPA_BASE_URL}/index.php?opcao=opt_05"

# Garantir que o diretório de dados exista
os.makedirs(DATA_DIR, exist_ok=True)
