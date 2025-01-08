"""
Configuration des tests pour les composants de chat.
"""
import pytest
from unittest.mock import Mock
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class DocumentReference:
    kb_id: str = ""
    doc_id: str = ""
    text: str = ""
    relevance_score: float = 0.0
    page_numbers: Tuple[int, int] = (0, 0)
    search_mode: str = "semantic"

@dataclass
class KnowledgeBase:
    id: str
    name: str
    description: str = ""

@pytest.fixture
def mock_kb():
    """Fixture pour le mock d'une base de connaissances."""
    kb = Mock()
    kb.id = "kb1"
    kb.name = "Test KB"
    kb.description = "Test Description"
    return kb

@pytest.fixture
def mock_document_reference():
    """Fixture pour le mock d'une référence de document."""
    return DocumentReference(
        kb_id="kb1",
        doc_id="doc1",
        text="Test content",
        relevance_score=0.9,
        page_numbers=(1, 2)
    )
