"""
Logique métier de base pour les filtres.
"""
from typing import List, Dict, Any, Callable, Optional
from src.pages.states.filter_state import FilterState
from src.pages.interfaces.filter import IFilterLogic

class BaseFilterLogic(IFilterLogic):
    """Logique métier de base pour le filtrage."""
    
    def __init__(self, title: str):
        """Initialise la logique de filtrage.
        
        Args:
            title: Titre du filtre
        """
        self.title = title
        
    def update_options(self, 
                      filter_state: FilterState,
                      items: List[Dict[str, Any]],
                      id_key: str = "id",
                      title_key: str = "title") -> None:
        """Met à jour les options du filtre.
        
        Args:
            filter_state: État du filtre
            items: Liste des éléments filtrables
            id_key: Clé pour l'identifiant dans les items
            title_key: Clé pour le titre dans les items
        """
        if not filter_state.initialized or len(filter_state.options) != len(items):
            filter_state.options = {
                str(item[id_key]): str(item[title_key]) 
                for item in items
            }
            # Sélectionner tous les éléments par défaut
            filter_state.selected_items = list(filter_state.options.keys())
            filter_state.initialized = True
    
    def get_selected_items(self, filter_state: FilterState) -> List[str]:
        """Récupère les éléments sélectionnés.
        
        Args:
            filter_state: État du filtre
            
        Returns:
            List[str]: IDs des éléments sélectionnés
        """
        return filter_state.selected_items
    
    def set_selected_items(self, filter_state: FilterState, selected_ids: List[str]) -> None:
        """Définit les éléments sélectionnés.
        
        Args:
            filter_state: État du filtre
            selected_ids: IDs à sélectionner
        """
        filter_state.selected_items = selected_ids
