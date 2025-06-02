"""
Módulo de inicialização para scrapers.
"""
from src.scrapers.base_scraper import BaseScraper
from src.scrapers.producao_scraper import ProducaoScraper
from src.scrapers.processamento_scraper import ProcessamentoScraper
from src.scrapers.comercializacao_scraper import ComercializacaoScraper
from src.scrapers.importacao_scraper import ImportacaoScraper
from src.scrapers.exportacao_scraper import ExportacaoScraper

__all__ = [
    'BaseScraper',
    'ProducaoScraper',
    'ProcessamentoScraper',
    'ComercializacaoScraper',
    'ImportacaoScraper',
    'ExportacaoScraper'
]
