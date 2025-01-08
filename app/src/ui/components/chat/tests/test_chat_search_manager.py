import unittest
from unittest.mock import Mock, patch
from dataclasses import dataclass

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

from src.ui.components.chat.chat_search_manager import ChatSearchManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class TestChatSearchManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.kb_manager = Mock(spec=KnowledgeBasesManager)
        self.search_manager = ChatSearchManager(self.kb_manager)

    def test_initialization(self):
        """Test the initialization of ChatSearchManager"""
        self.assertIsNotNone(self.search_manager.search_engine)
        self.assertEqual(self.search_manager.kb_manager, self.kb_manager)

    @patch('src.core.state_manager.StateManager.get_chat_state')
    def test_perform_search(self, mock_get_chat_state):
        """Test search functionality with mock knowledge bases"""
        # Configuration des mocks
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = ["kb1", "kb2"]
        mock_chat_state.selected_docs = ["doc1"]
        mock_get_chat_state.return_value = mock_chat_state

        # Configuration du mock kb_manager
        kb1 = KnowledgeBase(id="kb1", name="KB1")
        kb2 = KnowledgeBase(id="kb2", name="KB2")
        self.kb_manager.get_knowledge_base.side_effect = lambda x: {"kb1": kb1, "kb2": kb2}.get(x)

        # Configuration du mock search_engine
        expected_results = [
            DocumentReference(text="Result 1", relevance_score=0.9),
            DocumentReference(text="Result 2", relevance_score=0.8)
        ]
        self.search_manager.search_engine.search_knowledge_bases = Mock(return_value=expected_results)

        # Exécution de la recherche
        results = self.search_manager.perform_search("test query")

        # Vérifications
        self.assertEqual(results, expected_results)
        self.kb_manager.get_knowledge_base.assert_any_call("kb1")
        self.kb_manager.get_knowledge_base.assert_any_call("kb2")
        self.search_manager.search_engine.search_knowledge_bases.assert_called_once_with(
            query="test query",
            knowledge_bases=[kb1, kb2],
            selected_kbs=["kb1", "kb2"],
            selected_docs=["doc1"]
        )

    @patch('src.core.state_manager.StateManager.get_chat_state')
    @patch('streamlit.error')
    def test_perform_search_with_error(self, mock_error, mock_get_chat_state):
        """Test error handling during search"""
        # Configuration des mocks
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = ["kb1"]
        mock_chat_state.selected_docs = []
        mock_get_chat_state.return_value = mock_chat_state

        # Simulation d'une erreur dans search_engine
        error_message = "Search engine error"
        self.search_manager.search_engine.search_knowledge_bases = Mock(
            side_effect=Exception(error_message)
        )

        # Exécution de la recherche
        results = self.search_manager.perform_search("test query")

        # Vérifications
        mock_error.assert_called_once_with(f"Erreur lors de la recherche : {error_message}")

    @patch('src.core.state_manager.StateManager.get_chat_state')
    def test_perform_search_no_knowledge_bases(self, mock_get_chat_state):
        """Test search with no selected knowledge bases"""
        # Configuration des mocks
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = []
        mock_chat_state.selected_docs = []
        mock_get_chat_state.return_value = mock_chat_state

        # Configuration du mock search_engine
        self.search_manager.search_engine.search_knowledge_bases = Mock(return_value=[])

        # Exécution de la recherche
        results = self.search_manager.perform_search("test query")

        # Vérifications
        self.assertEqual(results, [])
        self.search_manager.search_engine.search_knowledge_bases.assert_called_once_with(
            query="test query",
            knowledge_bases=[],
            selected_kbs=[],
            selected_docs=[]
        )

if __name__ == '__main__':
    unittest.main()
