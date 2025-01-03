"""
Package core contenant les composants principaux de l'application.

Modules:
- knowledge_bases_manager: Gestion des bases de connaissances
- search_engine: Moteur de recherche
"""

from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.search_engine import SearchEngine

__all__ = [
    'KnowledgeBasesManager',
    'SearchEngine',
]
