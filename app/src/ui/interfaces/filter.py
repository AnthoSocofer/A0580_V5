"""
Interfaces pour les composants de filtrage.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.ui.states.filter_state import FilterState

class IFilterLogic(ABC):
    """Interface pour la logique de filtrage."""
    
    @abstractmethod
    def update_options(self, 
                      filter_state: FilterState,
                      items: List[Dict[str, Any]],
                      id_key: str = "id",
                      title_key: str = "title") -> None:
        """Met à jour les options du filtre."""
        pass
    
    @abstractmethod
    def get_selected_items(self, filter_state: FilterState) -> List[str]:
        """Récupère les éléments sélectionnés."""
        pass
    
    @abstractmethod
    def set_selected_items(self, filter_state: FilterState, selected_ids: List[str]) -> None:
        """Définit les éléments sélectionnés."""
        pass
