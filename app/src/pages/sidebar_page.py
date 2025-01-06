"""
Page de gestion des bases de connaissances.
"""
import streamlit as st
import logging
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.pages.components.llm_selector import LLMSelector
from src.pages.utils.kb_operations import KnowledgeBaseOperations
from src.pages.components.kb_expander import KnowledgeBaseCreator, KnowledgeBaseExpander

class KnowledgeBasePage:
    """Page de gestion des bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise la page avec le gestionnaire de bases."""
        self.kb_manager = kb_manager
        self.logger = logging.getLogger(__name__)
        self.llm_selector = LLMSelector()
        self.kb_operations = KnowledgeBaseOperations(kb_manager)
        self.kb_creator = KnowledgeBaseCreator(self.kb_operations)
        self.kb_expander = KnowledgeBaseExpander(self.kb_operations)
    
    def render(self):
        """Affiche la page de gestion des bases de connaissances."""
        
        # Création d'une nouvelle base
        with st.expander("Créer une nouvelle base", expanded=False):
            self.kb_creator.render_form()
        
        # Bases disponibles
        st.markdown("### Bases disponibles")
        
        # S'assurer que les bases sont chargées
        self.kb_operations.ensure_knowledge_bases_loaded()
        
        # Afficher la liste des bases
        self.kb_expander.render_list()
