"""
Gestionnaire des sources pour le chat.
"""
from typing import List, Dict, Any, Optional, cast
from src.core.types import DocumentReference
from src.ui.interfaces.chat import IChatSourceManager, Source
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
    
    def get_sources_for_message(self, message_id: str) -> List[Source]:
        """Récupère les sources pour un message.
        
        Args:
            message_id: ID du message
            
        Returns:
            Liste des sources associées au message
        """
        chat_state = StateManager.get_chat_state()
        if not chat_state.search_results:
            return []
            
        return self.format_sources(chat_state.search_results)
    
    def add_sources_to_message(self, message_id: str, sources: List[Source]) -> None:
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
    
    def format_sources(self, search_results: List[Dict[str, Any]]) -> List[Source]:
        """Formate les résultats de recherche en sources.
        
        Args:
            search_results: Résultats de recherche bruts
            
        Returns:
            Sources formatées avec les informations complètes
        """
        formatted_sources: List[Source] = []
        for result in search_results:
            kb_id = result.get("kb_id", "")
            doc_id = result.get("doc_id", "")
            
            # Récupérer les informations de la base et du document
            kb = self.kb_manager.get_knowledge_base(kb_id)
            if not kb:
                continue
                
            # Récupérer la liste des documents
            docs = self.kb_manager.list_documents(kb_id)
            doc = next((d for d in docs if d["doc_id"] == doc_id), None)
                
            if not doc:
                continue
                
            # Formater la source avec le type Source
            source = cast(Source, {
                "title": doc.get("title", doc_id),
                "kb_id": kb_id,
                "doc_id": doc_id,
                "page_numbers": result.get("page_numbers", []),
                "search_mode": result.get("search_mode", "semantic"),
                "score": float(result.get("score", 0)),
                "content": result.get("content", ""),
                "excerpt": result.get("text", "")
            })
            formatted_sources.append(source)
            
        return formatted_sources
    
    def format_references(self, references: List[DocumentReference]) -> List[Source]:
        """Formate les références de documents pour l'affichage.
        
        Args:
            references: Liste des références de documents
            
        Returns:
            Liste des sources formatées pour l'affichage
        """
        sources: List[Source] = []
        for ref in references:
            # Récupérer les informations du document
            docs = self.kb_manager.list_documents(ref.kb_id)
            doc_info = next(
                (doc for doc in docs if doc["doc_id"] == ref.doc_id),
                None
            )
            
            if not doc_info:
                continue
                
            # Formater la source
            source = cast(Source, {
                "title": doc_info.get("title", ref.doc_id),
                "kb_id": ref.kb_id,
                "doc_id": ref.doc_id,
                "page_numbers": ref.page_numbers,
                "search_mode": ref.search_mode,
                "score": ref.relevance_score,
                "content": ref.text,
                "excerpt": ref.text[:200] + "..." if len(ref.text) > 200 else ref.text
            })
            sources.append(source)
            
        return sources
    
    def _get_relevance_color(self, score: float) -> str:
        """Détermine la couleur d'affichage en fonction du score.
        
        Args:
            score: Score de pertinence
            
        Returns:
            Emoji de couleur correspondant au score
        """
        if score >= 0.8:
            return "🟢"  # Très pertinent
        elif score >= 0.6:
            return "🟡"  # Moyennement pertinent
        else:
            return "🔴"  # Peu pertinent
