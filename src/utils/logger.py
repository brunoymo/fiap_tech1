"""
Módulo de utilitários para logging.
"""
import logging
import os
from pathlib import Path

# Configuração do logger
def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Configura um logger com o nome e nível especificados.
    
    Args:
        name: Nome do logger
        log_file: Caminho para o arquivo de log (opcional)
        level: Nível de logging
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Formatar as mensagens de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Adicionar handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Adicionar handler para arquivo, se especificado
    if log_file:
        # Garantir que o diretório de logs exista
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
