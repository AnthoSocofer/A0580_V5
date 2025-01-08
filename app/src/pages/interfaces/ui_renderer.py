"""
Interfaces pour le rendu UI.
"""
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Callable, Iterator, ContextManager, BinaryIO

class IUIRenderer(ABC):
    """Interface pour le rendu UI."""
    
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
    def render_info(self, message: str) -> None:
        """Affiche un message d'information."""
        pass
    
    @abstractmethod
    def render_markdown(self, content: str) -> None:
        """Affiche du contenu markdown."""
        pass
    
    @abstractmethod
    def render_chat_input(self, placeholder: str) -> Optional[str]:
        """Affiche une zone de saisie de chat."""
        pass
    
    @abstractmethod
    def chat_message(self, role: str) -> ContextManager[None]:
        """Contexte pour un message de chat."""
        pass
    
    @abstractmethod
    def expander(self, label: str, expanded: bool = False) -> ContextManager[None]:
        """Contexte pour un expander."""
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
    def render_file_uploader(self,
                           label: str,
                           accepted_types: Optional[List[str]] = None) -> Optional[BinaryIO]:
        """Affiche un sélecteur de fichier."""
        pass
    
    @abstractmethod
    def render_button(self, label: str) -> bool:
        """Affiche un bouton."""
        pass
    
    @abstractmethod
    def render_text_input(self,
                         label: str,
                         value: str = "",
                         placeholder: str = "") -> str:
        """Affiche une zone de saisie de texte."""
        pass
    
    @abstractmethod
    def render_text_area(self,
                        label: str,
                        value: str = "",
                        placeholder: str = "") -> str:
        """Affiche une zone de saisie de texte multiligne."""
        pass
    
    @abstractmethod
    def columns(self, n: int) -> List[Any]:
        """Crée des colonnes."""
        pass
