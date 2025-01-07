"""
Application principale de l'Assistant Documentaire
"""
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.state_manager import StateManager
from src.pages.components.chat.chat_interface import ChatInterface
from src.pages.components.llm.llm_selector import LLMSelector
from src.pages.components.filters.kb_filter import KBFilter
from src.pages.components.filters.document_filter import DocumentFilter
from src.pages.components.kb.kb_interface import KBInterface
from src.config.load_config import load_config
from src.core.types import KnowledgeBase, Document

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
        
        # Initialisation des états
        StateManager.initialize_states()
        
        # Initialisation des composants
        self.chat_interface = ChatInterface(kb_manager=self.kb_manager)
        self.llm_selector = LLMSelector()
        self.kb_filter = KBFilter()
        self.doc_filter = DocumentFilter(kb_manager=self.kb_manager)
        self.kb_interface = KBInterface(self.kb_manager)
        
        # Chargement initial des bases de connaissances
        kb_state = StateManager.get_kb_state()
        raw_kbs = self.kb_manager.list_knowledge_bases()
        
        # Conversion des dictionnaires en objets KnowledgeBase
        kb_state.knowledge_bases = [
            KnowledgeBase(
                id=kb.get('kb_id', ''),
                title=kb.get('title', ''),
                description=kb.get('description', '')
            ) for kb in raw_kbs
        ]
        StateManager.update_kb_state(kb_state)
        
        # Effectuer une recherche initiale dans toutes les bases
        self._perform_initial_search()
    
    def _perform_initial_search(self):
        """Effectue une recherche initiale dans toutes les bases de connaissances."""
        chat_state = StateManager.get_chat_state()
        kb_state = StateManager.get_kb_state()
        
        # Sélectionner toutes les bases par défaut
        if kb_state.knowledge_bases:
            kb_ids = [kb.id for kb in kb_state.knowledge_bases]
            chat_state.selected_kbs = kb_ids
            StateManager.update_chat_state(chat_state)
    
    def _render_sidebar(self):
        """Affiche la barre latérale."""
        with st.sidebar:
            
            # Sélecteur de modèle LLM
            st.markdown("## Configuration du modèle")
            self.llm_selector.render()
            
            # Onglets de gestion
            st.markdown("## Gestion des bases")
            tab_filter, tab_kb = st.tabs(["Filtre", "Bases de connaissances"])
            with tab_filter:
                st.markdown("### Filtres de recherche")
                chat_state = StateManager.get_chat_state()
                kb_state = StateManager.get_kb_state()
                
                # Filtre des bases de connaissances
                self.kb_filter.render()
                
                # Filtre des documents
                self.doc_filter.render()
            with tab_kb:
                self.kb_interface.render()
            
            
    
    def render(self):
        """Affiche l'application."""
        # Affichage de la barre latérale
        self._render_sidebar()
        
        # Affichage de l'interface de chat
        self.chat_interface.render()

if __name__ == "__main__":
    app = App()
    app.render()
