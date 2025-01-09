"""
Interface pour le rendu des modèles LLM.
"""
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Callable
from src.ui.interfaces.renderers.form import IFormRenderer

class ILLMRenderer(IFormRenderer, ABC):
    """Interface pour le rendu des modèles LLM."""
    
    @abstractmethod
    def render_model_selector(self,
                            label: str,
                            models: List[Dict[str, Any]],
                            selected: Optional[str] = None,
                            on_change: Optional[Callable[[str], None]] = None) -> str:
        """Affiche un sélecteur de modèle LLM.
        
        Args:
            label: Label du sélecteur
            models: Liste des modèles disponibles
            selected: Modèle sélectionné par défaut
            on_change: Callback appelé lors d'un changement
            
        Returns:
            ID du modèle sélectionné
        """
        pass
    
    @abstractmethod
    def render_model_info(self, model_info: Dict[str, Any]) -> None:
        """Affiche les informations d'un modèle.
        
        Args:
            model_info: Informations du modèle à afficher
        """
        pass
    
    @abstractmethod
    def render_model_params(self,
                          params: Dict[str, Any],
                          on_change: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
        """Affiche les paramètres d'un modèle.
        
        Args:
            params: Paramètres actuels
            on_change: Callback appelé lors d'un changement
            
        Returns:
            Nouveaux paramètres
        """
        pass
    
    @abstractmethod
    def render_generation_status(self, status: Dict[str, Any]) -> None:
        """Affiche le statut de la génération.
        
        Args:
            status: Statut à afficher
        """
        pass
    
    @abstractmethod
    def render_token_counter(self, count: Dict[str, int]) -> None:
        """Affiche le compteur de tokens.
        
        Args:
            count: Décompte des tokens
        """
        pass
