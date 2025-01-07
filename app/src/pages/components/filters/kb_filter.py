"""
Filtre pour les bases de connaissances.
"""
from typing import List, Dict, Any, Callable
from src.pages.components.filters.base_filter import BaseFilter
from src.pages.states.filter_state import KBFilterState
from src.core.types import KnowledgeBase

class KBFilter(BaseFilter):
    """Composant de filtrage pour les bases de connaissances."""
    
    def __init__(self):
        """Initialise le filtre des bases de connaissances."""
        super().__init__("Bases de connaissances")
    
    def render_with_state(self,
                         filter_state: KBFilterState,
                         knowledge_bases: List[KnowledgeBase],
                         on_selection: Callable[[List[str]], None],
                         key_prefix: str = "") -> None:
        """Affiche le filtre avec son état.
        
        Args:
            filter_state: État du filtre
            knowledge_bases: Liste des bases de connaissances
            on_selection: Callback appelé lors d'une sélection
            key_prefix: Préfixe pour les clés Streamlit
        """
        # Conversion des KBs en format attendu par le filtre
        items = [
            {"id": kb.id, "title": kb.title}
            for kb in knowledge_bases
        ]
        
        self.render(
            filter_state=filter_state,
            items=items,
            on_selection=on_selection,
            key_prefix=key_prefix,
            placeholder="Sélectionner des bases de connaissances..."
        )
