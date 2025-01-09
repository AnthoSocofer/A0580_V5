"""
Interfaces pour le système de chat.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypedDict
from src.core.types import DocumentReference

class ChatMessage(TypedDict):
    """Structure des messages du chat."""
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]]
    id: Optional[str]

class Source(TypedDict):
    """Structure d'une source."""
    title: str
    kb_id: str
    doc_id: str
    page_numbers: List[int]
    search_mode: str
    score: float
    content: Optional[str]

class IChatSourceManager(ABC):
    """Interface pour le gestionnaire de sources."""
    
    @abstractmethod
    def get_sources_for_message(self, message_id: str) -> List[Source]:
        """Récupère les sources pour un message.
        
        Args:
            message_id: ID du message
            
        Returns:
            Liste des sources associées au message
        """
        pass
    
    @abstractmethod
    def add_sources_to_message(self, message_id: str, sources: List[Source]) -> None:
        """Ajoute des sources à un message.
        
        Args:
            message_id: ID du message
            sources: Sources à ajouter
        """
        pass
    
    @abstractmethod
    def format_sources(self, search_results: List[Dict[str, Any]]) -> List[Source]:
        """Formate les résultats de recherche en sources.
        
        Args:
            search_results: Résultats de recherche bruts
            
        Returns:
            Sources formatées avec les informations complètes
        """
        pass
    
    @abstractmethod
    def format_references(self, references: List[DocumentReference]) -> List[Source]:
        """Formate les références de documents pour l'affichage.
        
        Args:
            references: Liste des références de documents
            
        Returns:
            Liste des sources formatées pour l'affichage
        """
        pass

class IChatResponseGenerator(ABC):
    """Interface pour le générateur de réponses."""
    
    @abstractmethod
    def generate_response(self, 
                         prompt: str,
                         context: Optional[List[Dict[str, Any]]] = None) -> str:
        """Génère une réponse.
        
        Args:
            prompt: Message utilisateur
            context: Contexte optionnel (sources, historique, etc.)
            
        Returns:
            Réponse générée
        """
        pass

class IChatSearchManager(ABC):
    """Interface pour le gestionnaire de recherche."""
    
    @abstractmethod
    def search_relevant_content(self, 
                              query: str,
                              kb_ids: List[str]) -> List[Dict[str, Any]]:
        """Recherche du contenu pertinent.
        
        Args:
            query: Requête utilisateur
            kb_ids: Liste des IDs des bases de connaissances à chercher
            
        Returns:
            Résultats de recherche avec scores et métadonnées
        """
        pass
