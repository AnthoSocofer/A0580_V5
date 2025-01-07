"""
États liés aux bases de connaissances.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from src.core.types import KnowledgeBase
from src.pages.states.filter_state import KBFilterState

@dataclass
class KBState:
    """État des bases de connaissances."""
    knowledge_bases: List[KnowledgeBase] = field(default_factory=list)
    filter_state: KBFilterState = field(default_factory=KBFilterState)
    current_kb: Optional[KnowledgeBase] = None
    error_message: Optional[str] = None
    is_loading: bool = False
    
    def get_kb_by_id(self, kb_id: str) -> Optional[KnowledgeBase]:
        """Récupère une base de connaissances par son ID."""
        return next((kb for kb in self.knowledge_bases if kb.id == kb_id), None)
    
    def get_selected_kbs(self) -> List[KnowledgeBase]:
        """Récupère les bases de connaissances sélectionnées."""
        return [
            kb for kb in self.knowledge_bases 
            if kb.id in self.filter_state.selected_items
        ]

@dataclass
class KBCreationState:
    """État de création d'une base de connaissances."""
    title: str = ""
    description: str = ""
    kb_id: str = ""
    error_message: Optional[str] = None
    is_creating: bool = False
