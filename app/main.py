"""
Assistant Documentaire - Application principale
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.pages.components.kb.kb_interface import KBInterface
from src.pages.components.llm.llm_selector import LLMSelector
from src.pages.components.chat.chat_interface import ChatInterface
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
        
        # Initialisation des composants
        self.llm_selector = LLMSelector()
        self.kb_interface = KBInterface(self.kb_manager)
        self.chat_interface = ChatInterface()
        
    def render(self):
        """Affiche l'application."""
        # Barre latérale
        with st.sidebar:
            st.title("🤖 Assistant Documentaire")
            
            # Sélection du modèle LLM
            st.markdown("### Configuration du modèle")
            self.llm_selector.render()
            
            # Interface des bases de connaissances
            st.markdown("### Bases de connaissances")
            self.kb_interface.render()
        
        # Zone principale : chat
        self.chat_interface.render()

if __name__ == "__main__":
    app = App()
    app.render()
