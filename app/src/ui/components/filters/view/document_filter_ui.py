"""
Interface utilisateur pour le filtrage des documents.
"""
import streamlit as st
from src.ui.components.filters.business.document_filter_logic import DocumentFilterLogic
from src.ui.interfaces.ui_renderer import IUIRenderer

class DocumentFilterUI:
    """Interface utilisateur pour le filtrage des documents."""

    def __init__(self, filter_logic: DocumentFilterLogic, ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur de filtrage des documents."""
        self.filter_logic = filter_logic
        self.ui_renderer = ui_renderer

    def render(self):
        """Affiche l'interface de filtrage des documents."""
        # Récupérer les documents disponibles
        all_docs = self.filter_logic.get_available_documents()
        
        if not all_docs:
            st.info("Aucun document disponible dans les bases sélectionnées.")
            return
            
        # Créer les options pour la sélection
        doc_options = {doc['title']: doc['doc_id'] for doc in all_docs}
        selected_docs = self.filter_logic.get_selected_documents()
        
        # Sélection multiple de documents
        selected_doc_titles = self.ui_renderer.render_multiselect(
            label="Filtrer par documents",
            options=list(doc_options.keys()),
            default=[title for title, doc_id in doc_options.items() if doc_id in selected_docs]
        )
        
        # Mettre à jour les documents sélectionnés
        if selected_doc_titles is not None:
            new_selected_docs = [doc_options[title] for title in selected_doc_titles]
            self.filter_logic.handle_doc_selection(new_selected_docs)
