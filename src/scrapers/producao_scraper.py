"""
Scraper para dados de produção de uvas da Embrapa.
"""
import logging
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup
from src.scrapers.base_scraper import BaseScraper
from src.utils.config import PRODUCAO_URL
from src.utils.logger import setup_logger

# Configuração do logger
logger = setup_logger(__name__)

class ProducaoScraper(BaseScraper):
    """
    Classe para raspagem de dados de produção de uvas.
    """
    
    def __init__(self):
        """
        Inicializa o scraper de produção.
        """
        super().__init__(PRODUCAO_URL, "producao.json")
    
    def _parse_table(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extrai os dados da tabela de produção.
        
        Args:
            soup: Objeto BeautifulSoup com o HTML da página
            
        Returns:
            Lista de dicionários com os dados extraídos
        """
        try:
            logger.info("Extraindo dados da tabela de produção")
            
            # Encontra a tabela principal
            table = soup.find('table', {'class': 'tabela'})
            
            if not table:
                logger.error("Tabela de produção não encontrada")
                return []
            
            # Extrai os cabeçalhos
            headers = []
            header_row = table.find('tr', {'class': 'cab_tabela'})
            
            if header_row:
                for th in header_row.find_all('th'):
                    headers.append(th.text.strip())
            
            # Se não encontrou cabeçalhos, tenta outra abordagem
            if not headers:
                header_row = table.find('tr')
                if header_row:
                    for th in header_row.find_all(['th', 'td']):
                        headers.append(th.text.strip())
            
            # Extrai os dados das linhas
            data = []
            
            for row in table.find_all('tr')[1:]:  # Pula a linha de cabeçalho
                cells = row.find_all('td')
                
                if len(cells) >= len(headers):
                    row_data = {}
                    
                    for i, cell in enumerate(cells[:len(headers)]):
                        # Tenta converter para número se possível
                        value = cell.text.strip()
                        try:
                            if ',' in value:
                                # Converte número decimal com vírgula
                                value = float(value.replace('.', '').replace(',', '.'))
                            else:
                                # Tenta converter para inteiro
                                value = int(value)
                        except ValueError:
                            # Mantém como string se não for possível converter
                            pass
                        
                        row_data[headers[i]] = value
                    
                    data.append(row_data)
            
            return data
        except Exception as e:
            logger.error(f"Erro ao extrair dados da tabela: {str(e)}")
            return []
    
    def _extract_year(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extrai o ano de referência dos dados.
        
        Args:
            soup: Objeto BeautifulSoup com o HTML da página
            
        Returns:
            Ano de referência ou None em caso de erro
        """
        try:
            logger.info("Extraindo ano de referência")
            
            # Procura por elementos que possam conter o ano
            title = soup.find('div', {'id': 'titulo'})
            
            if title:
                text = title.text.strip()
                
                # Procura por um padrão de ano (4 dígitos)
                import re
                year_match = re.search(r'\b(19|20)\d{2}\b', text)
                
                if year_match:
                    return year_match.group(0)
            
            return None
        except Exception as e:
            logger.error(f"Erro ao extrair ano de referência: {str(e)}")
            return None
    
    def scrape(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Realiza a raspagem dos dados de produção.
        
        Args:
            filters: Dicionário com filtros a serem aplicados aos dados
            
        Returns:
            Dicionário com os dados raspados ou dados de fallback
        """
        soup = self.fetch_page()
        
        if not soup:
            logger.warning("Falha na raspagem, tentando carregar dados de fallback")
            fallback_data = self.load_from_fallback()
            return fallback_data if fallback_data else {"error": "Dados não disponíveis"}
        
        # Extrai o ano de referência
        year = self._extract_year(soup)
        
        # Extrai os dados da tabela
        table_data = self._parse_table(soup)
        
        # Extrai as subcategorias
        subcategories = self.get_subcategories(table_data)
        
        # Aplica filtros se fornecidos
        if filters:
            table_data = self.filter_data(table_data, filters)
        
        # Organiza os dados
        result = {
            "fonte": "Embrapa Vitivinicultura",
            "url": self.url,
            "ano_referencia": year,
            "data": table_data,
            "subcategorias": subcategories
        }
        
        # Salva os dados para fallback
        self.save_to_fallback(result)
        
        return result
