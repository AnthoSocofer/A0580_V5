"""
État de la conversation.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from src.ui.states.filter_state import DocumentFilterState

@dataclass
class ChatState:
    """État de la conversation."""
    messages: List[Dict[str, Any]] = field(default_factory=list)
    selected_kbs: List[str] = field(default_factory=list)
    selected_docs: List[str] = field(default_factory=list)
    is_processing: bool = False
    search_results: List[Dict[str, Any]] = field(default_factory=list)
    last_query: Optional[str] = None
    doc_filter_state: DocumentFilterState = field(default_factory=DocumentFilterState)
    error_message: Optional[str] = None
