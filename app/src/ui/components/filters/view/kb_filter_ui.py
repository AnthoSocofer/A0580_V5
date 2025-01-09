"""
Interface utilisateur pour le filtrage des bases de connaissances.
"""
import streamlit as st
from src.ui.components.filters.business.kb_filter_logic import KBFilterLogic
from src.ui.interfaces.ui_renderer import IUIRenderer

class KBFilterUI:
    """Interface utilisateur pour le filtrage des bases de connaissances."""

    def __init__(self, filter_logic: KBFilterLogic, ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur de filtrage des bases."""
        self.filter_logic = filter_logic
        self.ui_renderer = ui_renderer

    def render(self):
        """Affiche l'interface de filtrage des bases."""
        if not self.filter_logic.has_available_kbs():
            st.info("Aucune base de connaissances disponible.")
            return
            
        # Créer les options pour la sélection
        kb_options = self.filter_logic.get_kb_options()
        selected_options = self.filter_logic.get_selected_options()
        
        # Sélection multiple des bases
        selected_options = self.ui_renderer.render_multiselect(
            label="Bases de connaissances",
            options=list(kb_options.keys()),
            default=selected_options
        )
        
        # Mettre à jour les bases sélectionnées
        if selected_options is not None:
            self.filter_logic.update_selected_kbs(selected_options)
            
        # Note: La section Document a été supprimée car elle est déjà disponible dans l'onglet "Bases"
