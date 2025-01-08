"""
Interfaces pour la gestion d'état.
"""
from abc import ABC, abstractmethod
from src.ui.states.chat_state import ChatState
from src.ui.states.llm_state import LLMState
from src.ui.states.kb_state import KBState

class IStateManager(ABC):
    """Interface pour le gestionnaire d'état."""
    
    @abstractmethod
    def get_chat_state(self) -> ChatState:
        """Récupère l'état du chat."""
        pass
    
    @abstractmethod
    def get_llm_state(self) -> LLMState:
        """Récupère l'état du LLM."""
        pass
    
    @abstractmethod
    def get_kb_state(self) -> KBState:
        """Récupère l'état des bases de connaissances."""
        pass
    
    @abstractmethod
    def update_chat_state(self, chat_state: ChatState) -> None:
        """Met à jour l'état du chat."""
        pass
    
    @abstractmethod
    def update_llm_state(self, llm_state: LLMState) -> None:
        """Met à jour l'état du LLM."""
        pass
    
    @abstractmethod
    def update_kb_state(self, kb_state: KBState) -> None:
        """Met à jour l'état des bases de connaissances."""
        pass
