"""
Interfaces pour la logique métier des composants UI de gestion des bases de connaissances.
"""
from abc import abstractmethod
from typing import List, Dict, Any
from src.ui.interfaces.kb_infrastructure import IKnowledgeBaseProcessor

class IKBLogic(IKnowledgeBaseProcessor):
    """Interface pour la logique de gestion des bases de connaissances dans l'UI."""
    
    @abstractmethod
    def get_knowledge_bases(self) -> List[Dict[str, Any]]:
        """Récupère la liste des bases de connaissances."""
        pass
    
    @abstractmethod
    def upload_document(self, kb_id: str, file_content: bytes, filename: str) -> str:
        """Upload un document dans une base."""
        pass
    
    @abstractmethod
    def delete_document(self, kb_id: str, doc_id: str) -> None:
        """Supprime un document d'une base."""
        pass
    
    @abstractmethod
    def get_active_kb(self) -> str:
        """Récupère l'ID de la base active."""
        pass
    
    @abstractmethod
    def set_active_kb(self, kb_id: str) -> None:
        """Définit la base active."""
        pass
