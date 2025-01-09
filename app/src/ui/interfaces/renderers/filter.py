"""
Interface pour le rendu des filtres.
"""
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Callable

class IFilterRenderer(ABC):
    """Interface pour le rendu des filtres."""
    
    @abstractmethod
    def render_select(self, 
                     label: str,
                     options: List[str],
                     default: Optional[str] = None,
                     on_change: Optional[Callable] = None) -> str:
        """Rend un sélecteur.
        
        Args:
            label: Label du sélecteur
            options: Options disponibles
            default: Option sélectionnée par défaut
            on_change: Callback appelé lors d'un changement
            
        Returns:
            Option sélectionnée
        """
        pass
    
    @abstractmethod
    def render_multiselect(self,
                          label: str,
                          options: List[str],
                          default: Optional[List[str]] = None,
                          on_change: Optional[Callable] = None) -> List[str]:
        """Rend un sélecteur multiple.
        
        Args:
            label: Label du sélecteur
            options: Options disponibles
            default: Options sélectionnées par défaut
            on_change: Callback appelé lors d'un changement
            
        Returns:
            Options sélectionnées
        """
        pass
    
    @abstractmethod
    def render_filter_group(self,
                          label: str,
                          filters: List[Dict[str, Any]]) -> None:
        """Affiche un groupe de filtres.
        
        Args:
            label: Label du groupe
            filters: Liste des filtres à afficher
        """
        pass
    
    @abstractmethod
    def render_filter_summary(self, active_filters: Dict[str, Any]) -> None:
        """Affiche un résumé des filtres actifs.
        
        Args:
            active_filters: Filtres actuellement actifs
        """
        pass
    
    @abstractmethod
    def render_filter_actions(self,
                            on_clear: Optional[Callable] = None,
                            on_apply: Optional[Callable] = None) -> None:
        """Affiche les actions possibles sur les filtres.
        
        Args:
            on_clear: Callback pour réinitialiser les filtres
            on_apply: Callback pour appliquer les filtres
        """
        pass
