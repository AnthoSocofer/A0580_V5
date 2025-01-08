"""
Gestionnaire des sources pour le chat.
"""
from typing import List, Dict, Any
from src.core.types import DocumentReference
from src.ui.interfaces.chat import IChatSourceManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.state_manager import StateManager

class ChatSourceManager(IChatSourceManager):
    """Gestionnaire pour l'affichage et le formatage des sources."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise le gestionnaire de sources.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
    
    def get_sources_for_message(self, message_id: str) -> List[Dict[str, Any]]:
        """Récupère les sources pour un message.
        
        Args:
            message_id: ID du message
            
        Returns:
            List[Dict[str, Any]]: Liste des sources
        """
        chat_state = StateManager.get_chat_state()
        if not chat_state.search_results:
            return []
            
        return self.format_sources(chat_state.search_results)
    
    def add_sources_to_message(self, message_id: str, sources: List[Dict[str, Any]]) -> None:
        """Ajoute des sources à un message.
        
        Args:
            message_id: ID du message
            sources: Sources à ajouter
        """
        chat_state = StateManager.get_chat_state()
        for message in chat_state.messages:
            if message.get("id") == message_id:
                message["sources"] = sources
                StateManager.update_chat_state(chat_state)
                break
    
    def format_sources(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formate les résultats de recherche en sources.
        
        Args:
            search_results: Résultats de recherche
            
        Returns:
            List[Dict[str, Any]]: Sources formatées
        """
        formatted_sources = []
        for result in search_results:
            kb_id = result.get("kb_id")
            doc_id = result.get("doc_id")
            
            # Récupérer les informations de la base et du document
            kb = self.kb_manager.get_knowledge_base(kb_id)
            if not kb:
                continue
                
            # Récupérer la liste des documents
            docs = self.kb_manager.list_documents(kb_id)
            doc = next((d for d in docs if d["doc_id"] == doc_id), None)
                
            if not doc:
                continue
                
            # Formater la source
            source = {
                "title": doc.get("title", doc_id),
                "kb_id": kb_id,
                "doc_id": doc_id,
                "page_numbers": result.get("page_numbers", []),
                "search_mode": result.get("search_mode", "semantic"),
                "score": result.get("score", 0)
            }
            formatted_sources.append(source)
            
        return formatted_sources
