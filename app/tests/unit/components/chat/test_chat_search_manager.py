"""
Tests unitaires pour le gestionnaire de recherche du chat.
"""
import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import List, Tuple

from app.src.core.knowledge_bases_manager import KnowledgeBasesManager
from app.src.ui.components.chat.business.chat_search_manager import ChatSearchManager

@dataclass
class KnowledgeBase:
    id: str
    name: str
    description: str = ""

@dataclass
class DocumentReference:
    text: str
    relevance_score: float
    title: str = ""
    pages: str = ""

@pytest.fixture
def mock_kb():
    return KnowledgeBase(id="kb1", name="KB1")

@pytest.fixture
def mock_document_reference():
    return DocumentReference(text="Result 1", relevance_score=0.9)

class TestChatSearchManager:
    """Tests pour ChatSearchManager."""
    
    @pytest.fixture
    def search_manager(self, mock_kb):
        """Fixture pour le gestionnaire de recherche."""
        kb_manager = Mock(spec=KnowledgeBasesManager)
        kb_manager.get_knowledge_base.side_effect = lambda x: mock_kb if x == "kb1" else None
        return ChatSearchManager(kb_manager)

    def test_initialization(self, search_manager):
        """Test l'initialisation de ChatSearchManager."""
        assert search_manager.search_engine is not None
        assert search_manager.kb_manager is not None

    @patch('src.core.state_manager.StateManager.get_chat_state')
    def test_perform_search(self, mock_get_chat_state, search_manager, mock_document_reference):
        """Test la recherche avec des bases de connaissances."""
        # Configuration des mocks
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = ["kb1"]
        mock_chat_state.selected_docs = ["doc1"]
        mock_get_chat_state.return_value = mock_chat_state

        # Configuration du mock search_engine
        expected_results = [mock_document_reference]
        search_manager.search_engine.search_knowledge_bases = Mock(return_value=expected_results)

        # Exécution de la recherche
        results = search_manager.perform_search("test query")

        # Vérifications
        assert results == expected_results
        search_manager.kb_manager.get_knowledge_base.assert_called_once_with("kb1")
        search_manager.search_engine.search_knowledge_bases.assert_called_once()

    @patch('src.core.state_manager.StateManager.get_chat_state')
    @patch('streamlit.error')
    def test_perform_search_with_error(self, mock_error, mock_get_chat_state, search_manager):
        """Test la gestion des erreurs pendant la recherche."""
        # Configuration des mocks
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = ["kb1"]
        mock_chat_state.selected_docs = []
        mock_get_chat_state.return_value = mock_chat_state

        # Simulation d'une erreur dans search_engine
        error_message = "Search engine error"
        search_manager.search_engine.search_knowledge_bases = Mock(
            side_effect=Exception(error_message)
        )

        # Exécution de la recherche
        results = search_manager.perform_search("test query")

        # Vérifications
        mock_error.assert_called_once_with(f"Erreur lors de la recherche : {error_message}")

    @patch('src.core.state_manager.StateManager.get_chat_state')
    def test_perform_search_no_knowledge_bases(self, mock_get_chat_state, search_manager):
        """Test la recherche sans bases de connaissances."""
        # Configuration des mocks
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = []
        mock_chat_state.selected_docs = []
        mock_get_chat_state.return_value = mock_chat_state

        # Configuration du mock search_engine
        search_manager.search_engine.search_knowledge_bases = Mock(return_value=[])

        # Exécution de la recherche
        results = search_manager.perform_search("test query")

        # Vérifications
        assert results == []
        search_manager.search_engine.search_knowledge_bases.assert_called_once_with(
            query="test query",
            knowledge_bases=[],
            selected_kbs=[],
            selected_docs=[]
        )
