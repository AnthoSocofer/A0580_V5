"""
Assistant Documentaire - Application principale
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.pages.chat_page import ChatPage
from src.pages.sidebar_page import KnowledgeBasePage
from src.config.load_config import load_config
from src.core.state_manager import StateManager

# Chargement des variables d'environnement
load_dotenv()

class App:
    """Application principale de l'Assistant Documentaire."""
    
    def __init__(self):
        """Initialise l'application."""
        # Configuration de la page
        st.set_page_config(
            page_title="Assistant Documentaire",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Chargement de la configuration
        self.config = load_config()
        
        # Initialisation du gestionnaire de bases
        storage_dir = Path(self.config.knowledge_base.storage_directory).expanduser()
        self.kb_manager = KnowledgeBasesManager(storage_directory=str(storage_dir))
        
        # Initialisation des états via le StateManager
        StateManager.initialize_states()
        
        # Chargement initial des bases de connaissances
        kb_state = StateManager.get_kb_state()
        kb_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
        StateManager.update_kb_state(kb_state)
        
        # Initialisation des pages
        self.chat_page = ChatPage(kb_manager=self.kb_manager)
        self.kb_page = KnowledgeBasePage(self.kb_manager)
        
    def _render_sidebar(self):
        """Affiche la barre latérale."""
        with st.sidebar:
            # Sélecteur de modèle LLM
            st.markdown("## Sélection du modèle")
            self.chat_page.llm_selector.render()
            
            # Onglets de gestion
            st.markdown("## Gestion des Bases de Connaissances")
            tab_gestion, tab_chat = st.tabs([
                "Gestion Documentaire",
                "Filtres"
            ])
            
            # Affichage du contenu des onglets
            with tab_gestion:
                self.kb_page.render()
            
            with tab_chat:
                # S'assurer que les bases sont chargées pour les filtres
                kb_state = StateManager.get_kb_state()
                if kb_state.knowledge_bases is None:
                    kb_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
                    StateManager.update_kb_state(kb_state)
                self.chat_page.render_filters(kb_state.knowledge_bases, key_prefix="sidebar_")

    def render(self):
        """Affiche l'application."""
        # Affichage de la barre latérale
        self._render_sidebar()
        
        # Affichage de la page principale
        self.chat_page.render()

if __name__ == "__main__":
    app = App()
    app.render()