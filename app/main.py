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
        self.chat_interface = ChatInterface()
        self.llm_selector = LLMSelector()
        self.kb_filter = KBFilter()
        self.doc_filter = DocumentFilter()
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
            tab_kb, tab_filter = st.tabs(["Bases de connaissances", "Filtre"])
            
            with tab_kb:
                self.kb_interface.render()
            
            with tab_filter:
                st.markdown("### Filtres de recherche")
                chat_state = StateManager.get_chat_state()
                kb_state = StateManager.get_kb_state()
                
                # Filtre des bases de connaissances
                if kb_state.knowledge_bases:
                    self.kb_filter.render_with_state(
                        filter_state=kb_state.filter_state,
                        knowledge_bases=kb_state.knowledge_bases,
                        on_selection=lambda selected: self._handle_kb_selection(selected),
                        key_prefix="sidebar_"
                    )
                
                # Filtre des documents
                if chat_state.selected_kbs:
                    documents = []
                    for kb_id in chat_state.selected_kbs:
                        raw_docs = self.kb_manager.list_documents(kb_id)
                        # Conversion en objets Document
                        kb_docs = [
                            Document(
                                filename=doc.get('filename', ''),
                                title=doc.get('title', '') or doc.get('filename', ''),
                                description=doc.get('description', ''),
                                metadata=doc
                            ) for doc in raw_docs
                        ]
                        documents.extend(kb_docs)
                    
                    self.doc_filter.render_with_state(
                        filter_state=chat_state.doc_filter_state,
                        documents=documents,
                        on_selection=lambda selected: self._handle_doc_selection(selected),
                        key_prefix="sidebar_"
                    )
    
    def _handle_kb_selection(self, selected_kbs):
        """Gère la sélection des bases de connaissances."""
        chat_state = StateManager.get_chat_state()
        chat_state.selected_kbs = selected_kbs
        if not selected_kbs:
            chat_state.selected_docs = []
        StateManager.update_chat_state(chat_state)
    
    def _handle_doc_selection(self, selected_docs):
        """Gère la sélection des documents."""
        chat_state = StateManager.get_chat_state()
        chat_state.selected_docs = selected_docs
        StateManager.update_chat_state(chat_state)
    
    def render(self):
        """Affiche l'application."""
        # Affichage de la barre latérale
        self._render_sidebar()
        
        # Affichage de l'interface de chat
        self.chat_interface.render()

if __name__ == "__main__":
    app = App()
    app.render()
