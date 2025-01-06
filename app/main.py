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
        
        # Initialisation des pages
        self.chat_page = ChatPage(kb_manager=self.kb_manager)
        self.kb_page = KnowledgeBasePage(self.kb_manager)
        
        # Initialisation de l'état de session
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'selected_kbs' not in st.session_state:
            st.session_state.selected_kbs = []
        if 'selected_docs' not in st.session_state:
            st.session_state.selected_docs = []
        if 'kb_filter_initialized' not in st.session_state:
            st.session_state.kb_filter_initialized = False
        if 'current_tab' not in st.session_state:
            st.session_state.current_tab = "gestion"
    
    def _render_sidebar(self):
        """Affiche la barre latérale."""
        with st.sidebar:
            st.title("📚 Assistant Documentaire")
            
            # Sélecteur de modèle LLM
            self.chat_page.llm_selector.render()
            
            # Onglets de navigation
            tab_gestion, tab_chat = st.tabs([
                "Gestion Documentaire",
                "Filtres"
            ])
            
            # Chargement des bases une seule fois par session
            if 'knowledge_bases' not in st.session_state:
                st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
            
            # Affichage du contenu des onglets
            with tab_gestion:
                self.kb_page.render()
            
            with tab_chat:
                self.chat_page.render_filters(st.session_state.knowledge_bases, key_prefix="sidebar_")
            
            # Mise à jour de l'onglet actif
            if tab_gestion.id not in st.session_state or tab_chat.id not in st.session_state:
                st.session_state.current_tab = "gestion"
    
    def render(self):
        """Affiche l'application."""
        # Affichage de la barre latérale
        self._render_sidebar()
        
        # Affichage de la page principale
        self.chat_page.render()

if __name__ == "__main__":
    app = App()
    app.render()