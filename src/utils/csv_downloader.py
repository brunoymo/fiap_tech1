"""
Módulo de download de dados CSV da Embrapa.

Este módulo é responsável por baixar os arquivos CSV diretamente do site da Embrapa
e gerenciar o fallback para arquivos locais quando o download falhar.
"""
import os
import requests
import logging
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configurar logger
logger = logging.getLogger(__name__)

class CSVDownloader:
    """
    Classe para download e gerenciamento de arquivos CSV da Embrapa.
    """
    
    # URLs base para download dos arquivos CSV
    BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download"
    
    # Mapeamento de categorias para URLs de download (atualizado com os links fornecidos pelo usuário)
    DOWNLOAD_URLS = {
        "producao": "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv",
        "processamento_viniferas": "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv",
        "processamento_americanas": "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv",
        "processamento_mesa": "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv",
        "comercializacao": "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv",
        "importacao_vinho": "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv",
        "importacao_espumante": "http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv",
        "importacao_frescas": "http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv",
        "importacao_passas": "http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv",
        "importacao_suco": "http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv",
        "exportacao_vinho": "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv",
        "exportacao_espumante": "http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv",
        "exportacao_frescas": "http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv",
        "exportacao_suco": "http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv"
    }
    
    def __init__(self, data_dir: str):
        """
        Inicializa o downloader de CSV.
        
        Args:
            data_dir: Diretório base para armazenamento dos arquivos CSV
        """
        self.data_dir = data_dir
        self._ensure_directories()
    
    def _ensure_directories(self):
        """
        Garante que os diretórios para cada categoria existam.
        """
        for categoria in self.DOWNLOAD_URLS.keys():
            categoria_dir = os.path.join(self.data_dir, categoria)
            if not os.path.exists(categoria_dir):
                os.makedirs(categoria_dir)
                logger.info(f"Diretório criado: {categoria_dir}")
    
    def download_csv(self, categoria: str) -> Optional[str]:
        """
        Tenta baixar o arquivo CSV mais recente para a categoria especificada.
        
        Args:
            categoria: Nome da categoria (producao, processamento, etc.)
            
        Returns:
            Caminho para o arquivo CSV baixado ou None em caso de falha
        """
        if categoria not in self.DOWNLOAD_URLS:
            logger.error(f"Categoria inválida: {categoria}")
            return None
            
        url = self.DOWNLOAD_URLS[categoria]
        categoria_dir = os.path.join(self.data_dir, categoria)
        
        # Nome do arquivo com timestamp para evitar conflitos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{categoria}_{timestamp}.csv"
        filepath = os.path.join(categoria_dir, filename)
        
        try:
            logger.info(f"Tentando baixar CSV de {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                logger.info(f"CSV baixado com sucesso: {filepath}")
                return filepath
            else:
                logger.warning(f"Falha ao baixar CSV. Status code: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao baixar CSV: {str(e)}")
            return None
    
    def get_latest_csv(self, categoria: str) -> Optional[str]:
        """
        Obtém o caminho para o arquivo CSV mais recente da categoria.
        
        Args:
            categoria: Nome da categoria (producao, processamento, etc.)
            
        Returns:
            Caminho para o arquivo CSV mais recente ou None se não existir
        """
        categoria_dir = os.path.join(self.data_dir, categoria)
        
        if not os.path.exists(categoria_dir):
            logger.warning(f"Diretório não encontrado: {categoria_dir}")
            return None
            
        csv_files = [f for f in os.listdir(categoria_dir) if f.endswith('.csv')]
        
        if not csv_files:
            logger.warning(f"Nenhum arquivo CSV encontrado em {categoria_dir}")
            return None
            
        # Ordena por data de modificação (mais recente primeiro)
        csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(categoria_dir, x)), reverse=True)
        return os.path.join(categoria_dir, csv_files[0])
    
    def get_data(self, categoria: str, force_download: bool = False) -> Optional[Dict[str, Any]]:
        """
        Obtém os dados da categoria, tentando baixar primeiro e usando fallback se necessário.
        
        Args:
            categoria: Nome da categoria (producao, processamento, etc.)
            force_download: Se True, força o download mesmo que exista arquivo local
            
        Returns:
            Dicionário com os dados ou None em caso de falha
        """
        csv_path = None
        # Sempre tenta baixar o arquivo mais recente da web
        try:
            url = self.DOWNLOAD_URLS[categoria]
            logger.info(f"Lendo CSV diretamente da web: {url}")
            df = pd.read_csv(url, sep=';')
            # Extrai o ano do nome do arquivo ou usa o ano atual
            year = None
            import re
            year_match = re.search(r'(\d{4})', url)
            if year_match:
                year = year_match.group(1)
            else:
                year = str(datetime.now().year)
            data = df.to_dict('records')
            subcategorias = self._extract_subcategories(df)
            result = {
                "fonte": "Embrapa Vitivinicultura",
                "url": url,
                "ano_referencia": year,
                "data": data,
                "subcategorias": subcategorias
            }
            return result
        except Exception as e:
            logger.error(f"Erro ao ler CSV da web: {str(e)}. Tentando fallback local...")
            # Se falhar, tenta baixar e ler localmente
            csv_path = self.download_csv(categoria)
            if csv_path is None:
                csv_path = self.get_latest_csv(categoria)
                if csv_path:
                    logger.info(f"Usando arquivo CSV local: {csv_path}")
                else:
                    logger.error(f"Não foi possível obter dados para {categoria}")
                    return None
            try:
                return self._load_csv_data(csv_path, categoria)
            except Exception as e:
                logger.error(f"Erro ao carregar dados do CSV local: {str(e)}")
                return None
    
    def _load_csv_data(self, csv_path: str, categoria: str) -> Dict[str, Any]:
        """
        Carrega e processa os dados de um arquivo CSV.
        
        Args:
            csv_path: Caminho para o arquivo CSV
            categoria: Nome da categoria
            
        Returns:
            Dicionário com os dados processados
        """
        try:
            # Lê o CSV com separador ';'
            df = pd.read_csv(csv_path, sep=';')
            
            # Extrai o ano do nome do arquivo ou usa o ano atual
            year = None
            import re
            year_match = re.search(r'(\d{4})', os.path.basename(csv_path))
            if year_match:
                year = year_match.group(1)
            else:
                year = str(datetime.now().year)
            
            # Converte para lista de dicionários
            data = df.to_dict('records')
            
            # Extrai subcategorias
            subcategorias = self._extract_subcategories(df)
            
            # Organiza os dados no formato esperado
            result = {
                "fonte": "Embrapa Vitivinicultura",
                "url": "http://vitibrasil.cnpuv.embrapa.br/",
                "ano_referencia": year,
                "data": data,
                "subcategorias": subcategorias
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao processar CSV {csv_path}: {str(e)}")
            raise
    
    def _extract_subcategories(self, df: pd.DataFrame) -> Dict[str, List[Any]]:
        """
        Extrai as subcategorias dos dados do DataFrame.
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            Dicionário com as subcategorias
        """
        subcategorias = {}
        
        # Para cada coluna, extrai valores únicos como subcategorias
        for col in df.columns:
            if col.lower() not in ['quantidade', 'quantidade (l)', 'quantidade (l.)', 'quantidade (kg)']:
                valores = df[col].dropna().unique().tolist()
                subcategorias[col] = valores
        
        return subcategorias
