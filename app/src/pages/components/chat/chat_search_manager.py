"""
Gestionnaire de recherche pour l'interface de chat.
"""
from typing import List
import streamlit as st
from src.core.types import DocumentReference, KnowledgeBase
from src.core.search_engine import SearchEngine
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.state_manager import StateManager

class ChatSearchManager:
    """Gestionnaire pour la recherche dans les bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise le gestionnaire de recherche.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
        self.search_engine = SearchEngine()
    
    def perform_search(self, query: str) -> List[DocumentReference]:
        """Effectue une recherche documentaire.
        
        Args:
            query: Requête de recherche
            
        Returns:
            Liste des résultats de recherche
        """
        chat_state = StateManager.get_chat_state()
        
        # Récupérer les bases de connaissances actives
        knowledge_bases = []
        for kb_id in chat_state.selected_kbs:
            kb = self.kb_manager.get_knowledge_base(kb_id)
            if kb:
                knowledge_bases.append(kb)
        
        # Effectuer la recherche avec la nouvelle API
        try:
            results = self.search_engine.search_knowledge_bases(
                query=query,
                knowledge_bases=knowledge_bases,
                selected_kbs=chat_state.selected_kbs,
                selected_docs=chat_state.selected_docs
            )
            return results
        except Exception as e:
            st.error(f"Erreur lors de la recherche : {str(e)}")
            return []
