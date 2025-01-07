"""
Types communs utilisés dans l'application.
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class Document:
    """Document dans une base de connaissances."""
    filename: str
    title: str = ""
    description: str = ""
    page_count: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class KnowledgeBase:
    """Base de connaissances."""
    id: str
    title: str
    description: str = ""
    documents: List[Document] = field(default_factory=list)

@dataclass
class AutoContextConfig:
    """Configuration pour le contexte automatique."""
    chunk_size: int = 1000
    overlap: int = 200

@dataclass
class DocumentReference:
    """Référence à un document trouvé lors d'une recherche."""
    doc_id: str
    kb_id: str
    text: str
    relevance_score: float
    page_numbers: Tuple[int, int]
    search_mode: str
