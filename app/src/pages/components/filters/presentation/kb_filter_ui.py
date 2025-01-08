"""
Interface utilisateur pour le filtre des bases de connaissances.
"""
from typing import Optional
from src.pages.interfaces.ui_renderer import IUIRenderer
from src.pages.components.filters.domain.kb_filter_logic import KBFilterLogic

class KBFilterUI:
    """Interface utilisateur pour le filtre des bases de connaissances."""
    
    def __init__(self,
                 filter_logic: KBFilterLogic,
                 ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur."""
        self.filter_logic = filter_logic
        self.ui_renderer = ui_renderer
    
    def render(self) -> None:
        """Affiche l'interface de filtrage."""
        if not self.filter_logic.has_available_kbs():
            self.ui_renderer.render_info("Aucune base de connaissances disponible.")
            return
        
        # Récupération des options
        kb_options = list(self.filter_logic.get_kb_options().keys())
        selected_options = self.filter_logic.get_selected_options()
        
        # Affichage du sélecteur multiple
        new_selection = self.ui_renderer.render_multiselect(
            label="Bases de connaissances",
            options=kb_options,
            default=selected_options
        )
        
        # Mise à jour si la sélection a changé
        if set(new_selection) != set(selected_options):
            self.filter_logic.update_selected_kbs(new_selection)
