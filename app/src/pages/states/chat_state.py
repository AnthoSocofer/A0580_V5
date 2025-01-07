"""
État de la conversation.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ChatState:
    """État de la conversation."""
    messages: List[Dict[str, Any]] = field(default_factory=list)
    selected_kbs: List[str] = field(default_factory=list)
    selected_docs: List[str] = field(default_factory=list)
    kb_filter_initialized: bool = False
    kb_options: Dict[str, Any] = field(default_factory=dict)
    selected_kb_titles: List[str] = field(default_factory=list)
    cached_documents: Dict[str, Any] = field(default_factory=dict)
