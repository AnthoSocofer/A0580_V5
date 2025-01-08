"""
États des composants de filtrage.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime

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
    selected_date_range: str = "Tous"
    selected_size_range: str = "Tous"
    selected_types: List[str] = field(default_factory=lambda: ["Tous"])
    date_ranges: List[str] = field(default_factory=lambda: ["Tous", "Aujourd'hui", "Cette semaine", "Ce mois", "Cette année"])
    size_ranges: List[str] = field(default_factory=lambda: ["Tous", "<1Mo", "1-10Mo", ">10Mo"])
    document_types: List[str] = field(default_factory=lambda: ["Tous", "PDF", "Word", "Excel", "Image"])
