"""
Interface de base pour tous les renderers.
"""
from abc import ABC, abstractmethod
from typing import List, Any, Optional, ContextManager

class IBaseRenderer(ABC):
    """Interface de base pour tous les renderers."""
    
    @abstractmethod
    def render_info(self, message: str) -> None:
        """Affiche un message d'information."""
        pass
    
    @abstractmethod
    def render_success(self, message: str) -> None:
        """Affiche un message de succès."""
        pass
    
    @abstractmethod
    def render_error(self, message: str) -> None:
        """Affiche un message d'erreur."""
        pass
    
    @abstractmethod
    def render_markdown(self, content: str) -> None:
        """Affiche du contenu markdown."""
        pass
    
    @abstractmethod
    def columns(self, n: int) -> List[Any]:
        """Crée des colonnes."""
        pass
    
    @abstractmethod
    def expander(self, label: str, expanded: bool = False) -> ContextManager[None]:
        """Contexte pour un expander."""
        pass
