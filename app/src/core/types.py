"""
Types communs utilisés dans l'application.
"""
from typing import TypedDict, List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

class Document(TypedDict):
    """Document dans une base de connaissances."""
    doc_id: str
    title: str
    description: Optional[str]
    page_count: Optional[int]
    
class KnowledgeBase(TypedDict):
    """Base de connaissances."""
    kb_id: str
    title: str
    description: Optional[str]
    documents: List[Document]

class AutoContextConfig(TypedDict):
    """Configuration pour le contexte automatique."""
    use_generated_title: bool
    get_document_summary: bool
    get_section_summaries: bool

@dataclass
class DocumentReference:
    """Référence à un document trouvé lors d'une recherche."""
    doc_id: str
    kb_id: str
    text: str
    relevance_score: float
    page_numbers: Tuple[int, int]
    search_mode: str
