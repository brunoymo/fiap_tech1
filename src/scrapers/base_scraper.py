"""
Módulo base para scrapers da API de Vitivinicultura da Embrapa.
"""
import os
import json
import logging
from typing import Dict, Any, Optional, List
import requests
from bs4 import BeautifulSoup
from src.utils.config import DATA_DIR, REQUEST_TIMEOUT
from src.utils.logger import setup_logger

# Configuração do logger
logger = setup_logger(__name__)

class BaseScraper:
    """
    Classe base para scrapers da API de Vitivinicultura da Embrapa.
    """
    
    def __init__(self, url: str, fallback_file: str):
        """
        Inicializa o scraper.
        
        Args:
            url: URL da página a ser raspada
            fallback_file: Nome do arquivo de fallback
        """
        self.url = url
        self.fallback_file = os.path.join(DATA_DIR, fallback_file)
    
    def fetch_page(self) -> Optional[BeautifulSoup]:
        """
        Obtém a página HTML e retorna um objeto BeautifulSoup.
        
        Returns:
            Objeto BeautifulSoup ou None em caso de erro
        """
        try:
            logger.info(f"Obtendo página: {self.url}")
            response = requests.get(self.url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Erro ao obter página: {str(e)}")
            return None
    
    def save_to_fallback(self, data: Dict[str, Any]) -> bool:
        """
        Salva os dados em um arquivo JSON para fallback.
        
        Args:
            data: Dados a serem salvos
            
        Returns:
            True se os dados foram salvos com sucesso, False caso contrário
        """
        try:
            logger.info(f"Salvando dados de fallback em: {self.fallback_file}")
            os.makedirs(os.path.dirname(self.fallback_file), exist_ok=True)
            
            with open(self.fallback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar dados de fallback: {str(e)}")
            return False
    
    def load_from_fallback(self) -> Optional[Dict[str, Any]]:
        """
        Carrega os dados do arquivo JSON de fallback ou CSV alternativo.
        
        Returns:
            Dados carregados ou None em caso de erro
        """
        try:
            logger.info(f"Carregando dados de fallback de: {self.fallback_file}")
            
            # Tenta carregar do arquivo JSON padrão
            if os.path.exists(self.fallback_file):
                with open(self.fallback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Se não encontrar o JSON, tenta carregar do CSV alternativo
            csv_path = self.get_csv_fallback_path()
            if csv_path and os.path.exists(csv_path):
                logger.info(f"Arquivo JSON não encontrado, usando CSV alternativo: {csv_path}")
                return self.load_from_csv(csv_path)
                
            logger.warning(f"Nenhum arquivo de fallback encontrado")
            return None
        except Exception as e:
            logger.error(f"Erro ao carregar dados de fallback: {str(e)}")
            return None
            
    def get_csv_fallback_path(self) -> Optional[str]:
        """
        Obtém o caminho para o arquivo CSV alternativo com base no tipo de scraper.
        
        Returns:
            Caminho para o arquivo CSV ou None
        """
        # Extrai o tipo de dados do nome do arquivo de fallback
        fallback_name = os.path.basename(self.fallback_file)
        data_type = fallback_name.split('.')[0]  # Ex: "producao.json" -> "producao"
        
        # Constrói o caminho para o CSV
        csv_dir = os.path.join(os.path.dirname(os.path.dirname(self.fallback_file)), data_type)
        
        # Procura por arquivos CSV no diretório
        if os.path.exists(csv_dir):
            csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
            if csv_files:
                # Usa o CSV mais recente (assumindo que o nome contém o ano)
                csv_files.sort(reverse=True)
                return os.path.join(csv_dir, csv_files[0])
        
        return None
        
    def load_from_csv(self, csv_path: str) -> Dict[str, Any]:
        """
        Carrega dados de um arquivo CSV.
        
        Args:
            csv_path: Caminho para o arquivo CSV
            
        Returns:
            Dados carregados em formato de dicionário
        """
        try:
            import pandas as pd
            import datetime
            
            # Lê o CSV
            df = pd.read_csv(csv_path)
            
            # Converte para lista de dicionários
            data = df.to_dict('records')
            
            # Extrai o ano do nome do arquivo (assumindo formato como "producao_2023.csv")
            year = None
            filename = os.path.basename(csv_path)
            import re
            year_match = re.search(r'(\d{4})', filename)
            if year_match:
                year = year_match.group(1)
            
            # Organiza os dados no formato esperado
            result = {
                "fonte": "Embrapa Vitivinicultura (CSV local)",
                "url": "http://vitibrasil.cnpuv.embrapa.br/",
                "ano_referencia": year,
                "data": data,
                "subcategorias": self.get_subcategories(data)
            }
            
            return result
        except Exception as e:
            logger.error(f"Erro ao carregar dados do CSV: {str(e)}")
            
            # Retorna dados mínimos para evitar falha completa
            return {
                "fonte": "Embrapa Vitivinicultura (fallback mínimo)",
                "url": "http://vitibrasil.cnpuv.embrapa.br/",
                "ano_referencia": "2023",
                "data": [],
                "subcategorias": {}
            }
    
    def get_subcategories(self, data: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """
        Extrai as subcategorias dos dados raspados.
        
        Args:
            data: Lista de dicionários com os dados raspados
            
        Returns:
            Dicionário com as subcategorias disponíveis
        """
        subcategories = {}
        
        if not data:
            return subcategories
            
        # Obtém todas as chaves únicas dos dicionários
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
            
        # Para cada chave, extrai os valores únicos
        for key in all_keys:
            values = []
            for item in data:
                if key in item and item[key] not in values:
                    values.append(item[key])
            
            # Ordena os valores se possível
            try:
                values.sort()
            except:
                pass
                
            subcategories[key] = values
            
        return subcategories
    
    def filter_data(self, data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra os dados com base nos filtros fornecidos.
        
        Args:
            data: Lista de dicionários com os dados raspados
            filters: Dicionário com os filtros a serem aplicados
            
        Returns:
            Lista filtrada de dicionários
        """
        if not filters:
            return data
            
        filtered_data = []
        
        for item in data:
            match = True
            for key, value in filters.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            
            if match:
                filtered_data.append(item)
                
        return filtered_data
    
    def scrape(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Método principal para raspagem de dados.
        Deve ser implementado pelas classes filhas.
        
        Args:
            filters: Dicionário com filtros a serem aplicados aos dados
            
        Returns:
            Dados raspados em formato de dicionário
        """
        raise NotImplementedError("O método scrape deve ser implementado pelas classes filhas")
