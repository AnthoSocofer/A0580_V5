"""
Logique métier pour le filtre des bases de connaissances.
"""
from typing import Dict, List, Optional
from src.ui.interfaces.state_manager import IStateManager
from src.core.state_manager import StateManager

class KBFilterLogic:
    """Logique métier pour le filtre des bases de connaissances."""
    
    def __init__(self, state_manager: Optional[IStateManager] = None):
        """Initialise la logique de filtrage."""
        self.state_manager = state_manager or StateManager
        self._initialize_state()
    
    def _initialize_state(self) -> None:
        """Initialise l'état du filtre."""
        chat_state = self.state_manager.get_chat_state()
        if not hasattr(chat_state, 'selected_kbs'):
            chat_state.selected_kbs = []
        self.state_manager.update_chat_state(chat_state)
    
    def get_kb_options(self) -> Dict[str, str]:
        """Retourne les options de bases de connaissances disponibles."""
        kb_state = self.state_manager.get_kb_state()
        return {
            f"{kb.title} ({kb.id})": kb.id
            for kb in kb_state.knowledge_bases
        }
    
    def get_selected_options(self) -> List[str]:
        """Retourne les options actuellement sélectionnées."""
        chat_state = self.state_manager.get_chat_state()
        kb_options = self.get_kb_options()
        return [
            option
            for option, kb_id in kb_options.items()
            if kb_id in chat_state.selected_kbs
        ]
    
    def update_selected_kbs(self, selected_options: List[str]) -> None:
        """Met à jour les bases sélectionnées."""
        chat_state = self.state_manager.get_chat_state()
        kb_options = self.get_kb_options()
        
        chat_state.selected_kbs = [
            kb_options[option]
            for option in selected_options
        ]
        self.state_manager.update_chat_state(chat_state)
    
    def has_available_kbs(self) -> bool:
        """Vérifie si des bases sont disponibles."""
        kb_state = self.state_manager.get_kb_state()
        return len(kb_state.knowledge_bases) > 0
    
    def get_selected_kbs(self) -> List[str]:
        """Retourne la liste des IDs des bases sélectionnées."""
        chat_state = self.state_manager.get_chat_state()
        return chat_state.selected_kbs
