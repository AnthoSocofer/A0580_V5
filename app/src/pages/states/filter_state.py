"""
États des composants de filtrage.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class FilterState:
    """État générique pour un composant de filtrage."""
    selected_items: List[str] = field(default_factory=list)
    options: Dict[str, str] = field(default_factory=dict)
    initialized: bool = False

@dataclass
class KBFilterState(FilterState):
    """État spécifique pour le filtrage des bases de connaissances."""
    pass

@dataclass
class DocumentFilterState(FilterState):
    """État spécifique pour le filtrage des documents."""
    pass
