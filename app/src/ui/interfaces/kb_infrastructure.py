"""
Interfaces pour l'infrastructure de gestion des bases de connaissances.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from src.core.types import KnowledgeBase

class IKnowledgeBaseProcessor(ABC):
    """Interface pour le traitement des bases de connaissances."""
    
    @abstractmethod
    def create_knowledge_base(self, title: str, description: str) -> KnowledgeBase:
        """Crée une nouvelle base de connaissances."""
        pass
    
    @abstractmethod
    def update_knowledge_base(self, kb_id: str, title: str, description: str) -> KnowledgeBase:
        """Met à jour une base de connaissances."""
        pass
    
    @abstractmethod
    def delete_knowledge_base(self, kb_id: str) -> bool:
        """Supprime une base de connaissances."""
        pass

class IKnowledgeBaseStore(ABC):
    """Interface pour le stockage des bases de connaissances."""
    
    @abstractmethod
    def save_knowledge_base(self, kb: KnowledgeBase) -> str:
        """Sauvegarde une base de connaissances."""
        pass
    
    @abstractmethod
    def get_knowledge_base(self, kb_id: str) -> Optional[KnowledgeBase]:
        """Récupère une base de connaissances."""
        pass
    
    @abstractmethod
    def list_knowledge_bases(self) -> List[KnowledgeBase]:
        """Liste toutes les bases de connaissances."""
        pass
    
    @abstractmethod
    def delete_knowledge_base(self, kb_id: str) -> None:
        """Supprime une base de connaissances."""
        pass

class IKnowledgeBaseValidator(ABC):
    """Interface pour la validation des bases de connaissances."""
    
    @abstractmethod
    def validate_title(self, title: str) -> bool:
        """Valide le titre d'une base de connaissances."""
        pass
    
    @abstractmethod
    def validate_description(self, description: str) -> bool:
        """Valide la description d'une base de connaissances."""
        pass
    
    @abstractmethod
    def validate_knowledge_base(self, kb: KnowledgeBase) -> bool:
        """Valide une base de connaissances."""
        pass
