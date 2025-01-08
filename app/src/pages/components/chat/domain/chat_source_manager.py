"""
Gestionnaire des sources pour le chat.
"""
from typing import List, Dict, Any
from src.pages.interfaces.chat import IChatSourceManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager

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
        # Récupérer les sources depuis le gestionnaire de bases
        sources = []
        for kb_id in self.kb_manager.get_knowledge_bases():
            docs = self.kb_manager.get_documents(kb_id)
            for doc in docs:
                source = {
                    "title": doc.get("title", doc["doc_id"]),
                    "kb_id": kb_id,
                    "doc_id": doc["doc_id"]
                }
                sources.append(source)
        return sources
    
    def add_sources_to_message(self, message_id: str, sources: List[Dict[str, Any]]) -> None:
        """Ajoute des sources à un message.
        
        Args:
            message_id: ID du message
            sources: Sources à ajouter
        """
        # Cette méthode est gérée par le ChatLogic
        pass
    
    def format_sources(self, references: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formate les références pour l'affichage.
        
        Args:
            references: Liste des références
            
        Returns:
            List[Dict[str, Any]]: Sources formatées
        """
        sources = []
        for ref in references:
            kb_id = ref.get('kb_id')
            doc_id = ref.get('doc_id')
            
            # Récupérer les infos du document
            docs = self.kb_manager.get_documents(kb_id)
            doc_info = next(
                (doc for doc in docs if doc["doc_id"] == doc_id),
                None
            )
            
            if not doc_info:
                continue
                
            source = {
                "title": doc_info.get("title", doc_id),
                "excerpt": ref.get('excerpt', ''),
                "score": ref.get('score', 0),
                "kb_id": kb_id,
                "doc_id": doc_id,
                "pages": f"Pages {ref.get('page_start', 0)}-{ref.get('page_end', 0)}" if ref.get('page_start', 0) > 0 else "",
                "search_mode": ref.get('search_mode', 'standard')
            }
            sources.append(source)
        
        return sources
