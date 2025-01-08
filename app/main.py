"""
Application principale de l'Assistant Documentaire
"""
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from src.config.load_config import load_config
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager

from src.pages.components.chat.infrastructure.streamlit_chat_renderer import StreamlitChatRenderer
from src.pages.components.llm.infrastructure.streamlit_llm_renderer import StreamlitLLMRenderer
from src.pages.components.filters.infrastructure.streamlit_filter_renderer import StreamlitFilterRenderer
from src.pages.components.kb.infrastructure.streamlit_kb_renderer import StreamlitKBRenderer
from src.pages.components.document.infrastructure.streamlit_document_renderer import StreamlitDocumentRenderer

from src.pages.components.chat.domain.chat_logic import ChatLogic
from src.pages.components.llm.domain.llm_selector_logic import LLMSelectorLogic
from src.pages.components.filters.domain.kb_filter_logic import KBFilterLogic
from src.pages.components.filters.domain.document_filter_logic import DocumentFilterLogic
from src.pages.components.kb.domain.kb_manager_logic import KBManagerLogic
from src.pages.components.document.domain.document_manager_logic import DocumentManagerLogic

from src.pages.components.chat.presentation.chat_ui import ChatUI
from src.pages.components.llm.presentation.llm_selector_ui import LLMSelectorUI
from src.pages.components.filters.presentation.kb_filter_ui import KBFilterUI
from src.pages.components.filters.presentation.document_filter_ui import DocumentFilterUI
from src.pages.components.kb.presentation.kb_manager_ui import KBManagerUI
from src.pages.components.document.presentation.document_manager_ui import DocumentManagerUI

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
        
        # Initialisation des renderers Streamlit
        self.chat_renderer = StreamlitChatRenderer()
        self.llm_renderer = StreamlitLLMRenderer()
        self.filter_renderer = StreamlitFilterRenderer()
        self.kb_renderer = StreamlitKBRenderer()
        self.doc_renderer = StreamlitDocumentRenderer()
        
        # Initialisation des logiques métier
        self.chat_logic = ChatLogic(state_manager=StateManager)
        self.llm_logic = LLMSelectorLogic(state_manager=StateManager)
        self.kb_filter_logic = KBFilterLogic(state_manager=StateManager)
        self.doc_filter_logic = DocumentFilterLogic(
            state_manager=StateManager,
            kb_store=self.kb_manager
        )
        self.kb_logic = KBManagerLogic(
            state_manager=StateManager,
            kb_processor=self.kb_manager,
            kb_store=self.kb_manager,
            kb_validator=self.kb_manager
        )
        self.doc_logic = DocumentManagerLogic(
            state_manager=StateManager,
            document_processor=self.kb_manager,
            document_store=self.kb_manager,
            document_validator=self.kb_manager
        )
        
        # Initialisation des interfaces utilisateur
        self.chat_ui = ChatUI(self.chat_logic, self.chat_renderer)
        self.llm_ui = LLMSelectorUI(self.llm_logic, self.llm_renderer)
        self.kb_filter_ui = KBFilterUI(self.kb_filter_logic, self.filter_renderer)
        self.doc_filter_ui = DocumentFilterUI(self.doc_filter_logic, self.filter_renderer)
        self.kb_ui = KBManagerUI(self.kb_logic, self.kb_renderer)
        self.doc_ui = DocumentManagerUI(self.doc_logic, self.doc_renderer)
        
        # Chargement initial des bases de connaissances
        self._load_initial_knowledge_bases()
        
        # Effectuer une recherche initiale dans toutes les bases
        self._load_kb_initial_search()

    def _load_initial_knowledge_bases(self):
        """Charge les bases de connaissances initiales."""
        try:
            self.kb_logic.load_knowledge_bases()
        except Exception as e:
            st.error(f"Erreur lors du chargement des bases de connaissances: {str(e)}")

    def _load_kb_initial_search(self):
        """Effectue une recherche initiale dans toutes les bases de connaissances."""
        try:
            self.kb_filter_logic.search_all_knowledge_bases()
        except Exception as e:
            st.error(f"Erreur lors de la recherche initiale: {str(e)}")

    def _render_sidebar(self):
        """Affiche la barre latérale."""
        with st.sidebar:
            # Sélection du modèle LLM
            self.llm_ui.render()
            
            # Onglets des filtres
            tab_filters, tab_kb = st.tabs(["🔍 Filtres", "📚 Bases"])
            
            with tab_filters:
                st.markdown("### Filtres de recherche")
                # Filtre des bases de connaissances
                self.kb_filter_ui.render()
                # Filtre des documents
                self.doc_filter_ui.render()
            
            with tab_kb:
                self.kb_ui.render()

    def run(self):
        """Lance l'application."""
        self._render_sidebar()
        
        # Affichage de l'interface principale
        selected_kb = self.kb_filter_logic.get_selected_knowledge_base()
        if selected_kb:
            self.doc_ui.render(selected_kb)
            self.chat_ui.render()
        else:
            st.info("Veuillez sélectionner une base de connaissances pour commencer.")

if __name__ == "__main__":
    app = App()
    app.run()
