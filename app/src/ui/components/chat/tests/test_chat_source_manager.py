import unittest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class DocumentReference:
    kb_id: str
    doc_id: str
    text: str
    relevance_score: float
    page_numbers: Tuple[int, int]
    search_mode: str = "semantic"

from src.ui.components.chat.chat_source_manager import ChatSourceManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class TestChatSourceManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.kb_manager = Mock(spec=KnowledgeBasesManager)
        self.source_manager = ChatSourceManager(self.kb_manager)

    def test_initialization(self):
        """Test the initialization of ChatSourceManager"""
        self.assertEqual(self.source_manager.kb_manager, self.kb_manager)

    def test_format_sources(self):
        """Test formatting of document references"""
        # Préparation des données de test
        references = [
            DocumentReference(
                kb_id="kb1",
                doc_id="doc1",
                text="Test content 1",
                relevance_score=0.9,
                page_numbers=(1, 2)
            ),
            DocumentReference(
                kb_id="kb1",
                doc_id="doc2",
                text="Test content 2",
                relevance_score=0.7,
                page_numbers=(3, 4)
            )
        ]

        # Configuration du mock kb_manager
        mock_docs = [
            {"doc_id": "doc1", "title": "Document 1"},
            {"doc_id": "doc2", "title": "Document 2"}
        ]
        self.kb_manager.get_documents.return_value = mock_docs

        # Exécution du formatage
        formatted_sources = self.source_manager.format_sources(references)

        # Vérifications
        self.assertEqual(len(formatted_sources), 2)
        self.kb_manager.get_documents.assert_called_with("kb1")

        # Vérification du premier document formaté
        first_source = formatted_sources[0]
        self.assertEqual(first_source["title"], "Document 1")
        self.assertEqual(first_source["excerpt"], "Test content 1")
        self.assertEqual(first_source["score"], 0.9)
        self.assertEqual(first_source["pages"], "Pages 1-2")

    def test_format_sources_missing_doc(self):
        """Test formatting when document info is not found"""
        references = [
            DocumentReference(
                kb_id="kb1",
                doc_id="doc1",
                text="Test content",
                relevance_score=0.9,
                page_numbers=(1, 2)
            )
        ]

        # Configuration du mock kb_manager pour retourner une liste vide
        self.kb_manager.get_documents.return_value = []

        # Exécution du formatage
        formatted_sources = self.source_manager.format_sources(references)

        # Vérification qu'aucune source n'est retournée
        self.assertEqual(len(formatted_sources), 0)

    @patch('streamlit.expander')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.container')
    def test_render_sources(self, mock_container, mock_columns, mock_markdown, mock_expander):
        """Test rendering of sources"""
        segments = [
            DocumentReference(
                kb_id="kb1",
                doc_id="doc1",
                text="Test content 1",
                relevance_score=0.9,
                page_numbers=(1, 2)
            ),
            DocumentReference(
                kb_id="kb1",
                doc_id="doc2",
                text="Test content 2",
                relevance_score=0.7,
                page_numbers=(3, 4)
            )
        ]

        # Configuration des mocks streamlit
        mock_expander.return_value.__enter__.return_value = Mock()
        mock_container.return_value.__enter__.return_value = Mock()
        mock_columns.return_value = [Mock(), Mock(), Mock()]

        # Exécution du rendu
        self.source_manager.render_sources(segments)

        # Vérifications
        mock_expander.assert_called_once()
        self.assertEqual(mock_container.call_count, 2)

    @patch('streamlit.markdown')
    def test_render_source_summary(self, mock_markdown):
        """Test rendering of source summary"""
        segments = [
            DocumentReference(
                kb_id="kb1",
                doc_id="doc1",
                text="Test content 1",
                relevance_score=0.9,
                page_numbers=(1, 2)
            ),
            DocumentReference(
                kb_id="kb1",
                doc_id="doc2",
                text="Test content 2",
                relevance_score=0.4,
                page_numbers=(3, 4)
            )
        ]

        # Exécution du rendu du résumé
        self.source_manager.render_source_summary(segments)

        # Vérification que seule la source pertinente (score >= 0.5) est affichée
        self.assertEqual(mock_markdown.call_count, 3)  # 2 appels pour les en-têtes + 1 pour la source

if __name__ == '__main__':
    unittest.main()
