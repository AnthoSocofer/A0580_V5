"""
Interface utilisateur pour le filtrage des documents.
"""
import streamlit as st
from src.pages.components.filters.domain.document_filter_logic import DocumentFilterLogic
from src.pages.interfaces.ui_renderer import IUIRenderer

class DocumentFilterUI:
    """Interface utilisateur pour le filtrage des documents."""

    def __init__(self, filter_logic: DocumentFilterLogic, ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur de filtrage des documents."""
        self.filter_logic = filter_logic
        self.ui_renderer = ui_renderer

    def render(self):
        """Affiche l'interface de filtrage des documents."""
        st.markdown("#### Types de documents")
        
        # Sélection des types de documents
        selected_types = self.ui_renderer.render_multiselect(
            label="Types",
            options=self.filter_logic.get_available_document_types(),
            default=self.filter_logic.get_selected_document_types()
        )
        
        if selected_types:
            self.filter_logic.set_selected_document_types(selected_types)
