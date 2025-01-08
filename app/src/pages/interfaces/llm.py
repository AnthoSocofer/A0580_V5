"""
Interfaces pour les composants LLM.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class ILLMSelector(ABC):
    """Interface pour le sélecteur de LLM."""
    
    @abstractmethod
    def get_llm(self) -> Any:
        """Retourne l'instance LLM appropriée."""
        pass
    
    @abstractmethod
    def get_providers(self) -> List[str]:
        """Retourne la liste des fournisseurs disponibles."""
        pass
    
    @abstractmethod
    def get_models_for_provider(self, provider: str) -> List[str]:
        """Retourne la liste des modèles pour un fournisseur."""
        pass
    
    @abstractmethod
    def get_current_selection(self) -> Dict[str, str]:
        """Retourne la sélection actuelle."""
        pass
    
    @abstractmethod
    def update_selection(self, provider: str, model: str) -> None:
        """Met à jour la sélection."""
        pass
