"""
Interface pour les composants de formulaire.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Callable, ContextManager

class IFormRenderer(ABC):
    """Interface pour les composants de formulaire."""
    
    @abstractmethod
    def render_text_input(self,
                         label: str,
                         value: str = "",
                         placeholder: str = "",
                         key: Optional[str] = None,
                         help: Optional[str] = None) -> str:
        """Affiche une zone de saisie de texte."""
        pass
    
    @abstractmethod
    def render_text_area(self,
                        label: str,
                        value: str = "",
                        placeholder: str = "",
                        key: Optional[str] = None,
                        help: Optional[str] = None) -> str:
        """Affiche une zone de saisie de texte multiligne."""
        pass
    
    @abstractmethod
    def render_select(self,
                     label: str,
                     options: List[str],
                     default: Optional[str] = None,
                     on_change: Optional[Callable] = None) -> str:
        """Rend un sélecteur."""
        pass
    
    @abstractmethod
    def render_multiselect(self,
                          label: str,
                          options: List[str],
                          default: Optional[List[str]] = None,
                          on_change: Optional[Callable] = None) -> List[str]:
        """Rend un sélecteur multiple."""
        pass
    
    @abstractmethod
    def render_button(self, label: str, key: Optional[str] = None) -> bool:
        """Rend un bouton."""
        pass
    
    @abstractmethod
    def render_form_submit_button(self, label: str) -> bool:
        """Affiche un bouton de soumission de formulaire."""
        pass
    
    @abstractmethod
    def form(self, key: str) -> ContextManager[None]:
        """Contexte pour un formulaire."""
        pass
