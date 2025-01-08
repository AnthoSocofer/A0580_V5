"""
Tests unitaires pour le gestionnaire de sources du chat.
"""
import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class DocumentReference:
    kb_id: str = "kb1"
    doc_id: str = "doc1"
    text: str = "Test content 1"
    relevance_score: float = 0.9
    page_numbers: Tuple[int, int] = (1, 2)
    search_mode: str = "semantic"

from app.src.core.knowledge_bases_manager import KnowledgeBasesManager
from app.src.ui.components.chat.business.chat_source_manager import ChatSourceManager

@pytest.fixture
def mock_document_reference():
    return DocumentReference(
        kb_id="kb1",
        doc_id="doc1",
        text="Test content 1",
        relevance_score=0.9,
        page_numbers=(1, 2)
    )

class TestChatSourceManager:
    """Tests pour ChatSourceManager."""
    
    @pytest.fixture
    def source_manager(self):
        """Fixture pour le gestionnaire de sources."""
        kb_manager = Mock(spec=KnowledgeBasesManager)
        return ChatSourceManager(kb_manager)

    def test_initialization(self, source_manager):
        """Test l'initialisation de ChatSourceManager."""
        assert source_manager.kb_manager is not None

    def test_format_sources(self, source_manager, mock_document_reference):
        """Test le formatage des références de documents."""
        # Préparation des données de test
        references = [
            mock_document_reference,
            mock_document_reference._replace(
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
        source_manager.kb_manager.get_documents.return_value = mock_docs

        # Exécution du formatage
        formatted_sources = source_manager.format_sources(references)

        # Vérifications
        assert len(formatted_sources) == 2
        source_manager.kb_manager.get_documents.assert_called_with("kb1")

        # Vérification du premier document formaté
        first_source = formatted_sources[0]
        assert first_source["title"] == "Document 1"
        assert first_source["excerpt"] == "Test content 1"
        assert first_source["score"] == 0.9
        assert first_source["pages"] == "Pages 1-2"

    def test_format_sources_missing_doc(self, source_manager, mock_document_reference):
        """Test le formatage quand l'information du document est manquante."""
        references = [mock_document_reference]

        # Configuration du mock kb_manager pour retourner une liste vide
        source_manager.kb_manager.get_documents.return_value = []

        # Exécution du formatage
        formatted_sources = source_manager.format_sources(references)

        # Vérification qu'aucune source n'est retournée
        assert len(formatted_sources) == 0

    @patch('streamlit.expander')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.container')
    def test_render_sources(self, mock_container, mock_columns, mock_markdown, mock_expander, source_manager, mock_document_reference):
        """Test le rendu des sources."""
        segments = [
            mock_document_reference,
            mock_document_reference._replace(
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
        source_manager.render_sources(segments)

        # Vérifications
        mock_expander.assert_called_once()
        assert mock_container.call_count == 2

    @patch('streamlit.markdown')
    def test_render_source_summary(self, mock_markdown, source_manager, mock_document_reference):
        """Test le rendu du résumé des sources."""
        segments = [
            mock_document_reference,
            mock_document_reference._replace(
                text="Test content 2",
                relevance_score=0.4,
                page_numbers=(3, 4)
            )
        ]

        # Exécution du rendu du résumé
        source_manager.render_source_summary(segments)

        # Vérification que seule la source pertinente (score >= 0.5) est affichée
        assert mock_markdown.call_count == 3  # 2 appels pour les en-têtes + 1 pour la source
