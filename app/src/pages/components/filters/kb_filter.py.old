"""
Filtre pour les bases de connaissances.
"""
import streamlit as st
from typing import List, Dict, Any
from src.core.state_manager import StateManager
from src.core.types import KnowledgeBase

class KBFilter:
    """Filtre de sélection des bases de connaissances."""
    
    def render(self):
        """Affiche le filtre des bases de connaissances."""
        chat_state = StateManager.get_chat_state()
        kb_state = StateManager.get_kb_state()
        
        if not kb_state.knowledge_bases:
            st.info("Aucune base de connaissances disponible.")
            return
            
        # Créer les options pour la sélection
        kb_options = {
            f"{kb.title} ({kb.id})": kb.id
            for kb in kb_state.knowledge_bases
        }
        
        # Sélection multiple des bases
        selected_options = st.multiselect(
            "Bases de connaissances",
            options=list(kb_options.keys()),
            default=[
                option for option, kb_id in kb_options.items()
                if kb_id in chat_state.selected_kbs
            ],
            format_func=lambda x: x
        )
        
        # Mettre à jour l'état avec les bases sélectionnées
        chat_state.selected_kbs = [
            kb_options[option]
            for option in selected_options
        ]
        StateManager.update_chat_state(chat_state)
