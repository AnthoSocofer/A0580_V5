"""
Opérations sur les bases de connaissances.
"""
import streamlit as st
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.types import KnowledgeBase

class KnowledgeBaseOperations:
    """Opérations sur les bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise les opérations avec le gestionnaire de bases."""
        self.kb_manager = kb_manager
    
    def ensure_knowledge_bases_loaded(self) -> None:
        """S'assure que les bases sont chargées dans l'état."""
        kb_state = StateManager.get_kb_state()
        if not kb_state.knowledge_bases:
            kb_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
            StateManager.update_kb_state(kb_state)
    
    def create_knowledge_base(self, kb_id: str, title: str, description: str = "") -> None:
        """Crée une nouvelle base de connaissances."""
        try:
            # Créer la base
            self.kb_manager.create_knowledge_base(kb_id, title, description)
            
            # Mettre à jour l'état
            kb_state = StateManager.get_kb_state()
            kb_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
            StateManager.update_kb_state(kb_state)
            
            st.success(f"Base '{title}' créée avec succès!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur lors de la création: {str(e)}")
    
    def select_knowledge_base(self, kb_id: str) -> None:
        """Sélectionne une base de connaissances."""
        try:
            # Charger la base
            kb = self.kb_manager.get_knowledge_base(kb_id)
            
            # Mettre à jour l'état
            kb_state = StateManager.get_kb_state()
            kb_state.current_kb = kb
            kb_state.current_kb_id = kb_id
            StateManager.update_kb_state(kb_state)
            
        except Exception as e:
            st.error(f"Erreur lors de la sélection: {str(e)}")
    
    def delete_knowledge_base(self, kb_id: str) -> None:
        """Supprime une base de connaissances."""
        try:
            # Supprimer la base
            self.kb_manager.delete_knowledge_base(kb_id)
            
            # Mettre à jour l'état
            kb_state = StateManager.get_kb_state()
            kb_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
            if kb_state.current_kb_id == kb_id:
                kb_state.current_kb = None
                kb_state.current_kb_id = None
            StateManager.update_kb_state(kb_state)
            
            st.success(f"Base '{kb_id}' supprimée avec succès!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {str(e)}")
    
    def handle_expander_change(self, kb_id: str, is_expanded: bool) -> None:
        """Gère le changement d'état d'un expander."""
        kb_state = StateManager.get_kb_state()
        if is_expanded:
            if kb_state.active_expander != kb_id:
                kb_state.active_expander = kb_id
                StateManager.update_kb_state(kb_state)
                self.select_knowledge_base(kb_id)
        elif kb_state.active_expander == kb_id:
            kb_state.active_expander = None
            kb_state.current_kb = None
            kb_state.current_kb_id = None
            StateManager.update_kb_state(kb_state)
