"""
Endpoint para subcategorias de todas as categorias.
"""
from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Dict, Any
from src.utils.csv_downloader import CSVDownloader
from src.utils.filter_parser import parse_filters
import os
import logging

router = APIRouter(prefix="/subcategorias", tags=["Subcategorias"])

# Inicializa o downloader de CSV
csv_downloader = CSVDownloader(data_dir="/tmp")
logger = logging.getLogger(__name__)

# Endpoint removido
