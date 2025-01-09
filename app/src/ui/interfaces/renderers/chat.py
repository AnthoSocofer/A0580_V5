"""
Interface pour le rendu du chat.
"""
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Optional, List, Any

class IChatRenderer(ABC):
    """Interface pour le rendu du chat."""

    @abstractmethod
    def render_markdown(self, text: str) -> None:
        """Affiche du texte formaté en markdown.
        
        Args:
            text: Texte à afficher
        """
        pass
        
    @abstractmethod
    def render_info(self, text: str) -> None:
        """Affiche un message d'information.
        
        Args:
            text: Message à afficher
        """
        pass
        
    @abstractmethod
    def render_chat_input(self, placeholder: str) -> Optional[str]:
        """Affiche une zone de saisie pour le chat.
        
        Args:
            placeholder: Texte indicatif
            
        Returns:
            Le texte saisi par l'utilisateur ou None
        """
        pass
        
    @abstractmethod
    def chat_message(self, role: str) -> AbstractContextManager[None]:
        """Crée un contexte pour afficher un message.
        
        Args:
            role: Rôle de l'émetteur (user/assistant)
            
        Returns:
            Gestionnaire de contexte
        """
        pass
        
    @abstractmethod
    def expander(self, label: str, expanded: bool = False) -> AbstractContextManager[None]:
        """Crée un contexte pour un élément dépliable.
        
        Args:
            label: Texte du bouton
            expanded: True si déplié par défaut
            
        Returns:
            Gestionnaire de contexte
        """
        pass
        
    @abstractmethod
    def container(self) -> AbstractContextManager[None]:
        """Crée un conteneur pour grouper des éléments.
        
        Returns:
            Gestionnaire de contexte
        """
        pass
        
    @abstractmethod
    def columns(self, n: int) -> List[Any]:
        """Crée des colonnes pour l'affichage.
        
        Args:
            n: Nombre de colonnes
            
        Returns:
            Liste des colonnes
        """
        pass
        
    @abstractmethod
    def render_code(self, code: str, language: str = "python") -> None:
        """Affiche du code avec coloration syntaxique.
        
        Args:
            code: Code à afficher
            language: Langage pour la coloration
        """
        pass
        
    @abstractmethod
    def render_divider(self) -> None:
        """Affiche une ligne de séparation."""
        pass
