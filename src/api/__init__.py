"""
Módulo de inicialização para a API.
"""
from fastapi import APIRouter
from src.api.endpoints import router

__all__ = ['router']
