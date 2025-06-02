"""
Função utilitária para parsear filtros de query parameters.
"""
from fastapi import Query
from typing import Dict, Any, Optional

def parse_filters(q: Optional[str] = Query(None, description="Filtros no formato 'chave1=valor1,chave2=valor2'")):
    """
    Converte uma string de query params em um dicionário de filtros.
    """
    if not q:
        return None
    filters = {}
    try:
        for filter_item in q.split(','):
            if '=' in filter_item:
                key, value = filter_item.split('=', 1)
                # Tenta converter para número se possível
                try:
                    if '.' in value:
                        value = float(value.replace('.', '').replace(',', '.'))
                    else:
                        value = int(value)
                except ValueError:
                    # Mantém como string se não for possível converter
                    pass
                filters[key] = value
        return filters
    except Exception:
        return None 