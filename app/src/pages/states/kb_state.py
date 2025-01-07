"""
États liés aux bases de connaissances.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from src.core.types import KnowledgeBase, Document

@dataclass
class KBState:
    """État des bases de connaissances."""
    current_kb: Optional[KnowledgeBase] = None
    current_kb_id: Optional[str] = None
    active_expander: Optional[str] = None
    knowledge_bases: List[KnowledgeBase] = field(default_factory=list)
    uploaded_files: List[Any] = field(default_factory=list)
    
@dataclass
class KBCreationState:
    """État de création d'une base de connaissances."""
    title: str = ""
    description: str = ""
    kb_id: str = ""
    error_message: Optional[str] = None
    is_creating: bool = False
