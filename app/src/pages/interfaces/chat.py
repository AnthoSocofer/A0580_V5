"""
Interfaces pour le système de chat.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IChatMessage:
    """Interface pour les messages du chat."""
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None

class IChatSourceManager(ABC):
    """Interface pour le gestionnaire de sources."""
    
    @abstractmethod
    def get_sources_for_message(self, message_id: str) -> List[Dict[str, Any]]:
        """Récupère les sources pour un message."""
        pass
    
    @abstractmethod
    def add_sources_to_message(self, message_id: str, sources: List[Dict[str, Any]]) -> None:
        """Ajoute des sources à un message."""
        pass

class IChatResponseGenerator(ABC):
    """Interface pour le générateur de réponses."""
    
    @abstractmethod
    def generate_response(self, 
                         prompt: str,
                         context: Optional[List[Dict[str, Any]]] = None) -> str:
        """Génère une réponse."""
        pass

class IChatSearchManager(ABC):
    """Interface pour le gestionnaire de recherche."""
    
    @abstractmethod
    def search_relevant_content(self, 
                              query: str,
                              kb_ids: List[str]) -> List[Dict[str, Any]]:
        """Recherche du contenu pertinent."""
        pass
