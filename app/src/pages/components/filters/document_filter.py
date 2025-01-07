"""
Filtre pour les documents.
"""
from typing import List, Dict, Any, Callable
from src.pages.components.filters.base_filter import BaseFilter
from src.pages.states.filter_state import DocumentFilterState
from src.core.types import Document

class DocumentFilter(BaseFilter):
    """Composant de filtrage pour les documents."""
    
    def __init__(self):
        """Initialise le filtre des documents."""
        super().__init__("Documents")
    
    def render_with_state(self,
                         filter_state: DocumentFilterState,
                         documents: List[Document],
                         on_selection: Callable[[List[str]], None],
                         key_prefix: str = "") -> None:
        """Affiche le filtre avec son état.
        
        Args:
            filter_state: État du filtre
            documents: Liste des documents
            on_selection: Callback appelé lors d'une sélection
            key_prefix: Préfixe pour les clés Streamlit
        """
        # Conversion des documents en format attendu par le filtre
        items = [
            {"id": doc.id, "title": doc.title or doc.filename}
            for doc in documents
        ]
        
        self.render(
            filter_state=filter_state,
            items=items,
            on_selection=on_selection,
            key_prefix=key_prefix,
            placeholder="Sélectionner des documents..."
        )
