"""
Tests unitaires pour le générateur de réponses du chat.
"""
import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import List, Tuple

from app.src.core.knowledge_bases_manager import KnowledgeBasesManager
from app.src.ui.components.chat.business.chat_response_generator import ChatResponseGenerator

@dataclass
class DocumentReference:
    text: str
    relevance_score: float
    title: str = ""
    pages: str = ""

@pytest.fixture
def mock_document_reference():
    return DocumentReference(text="Paris est la capitale de la France.", relevance_score=0.9)

class TestChatResponseGenerator:
    """Tests pour ChatResponseGenerator."""
    
    @pytest.fixture
    def response_generator(self):
        """Fixture pour le générateur de réponses."""
        return ChatResponseGenerator()

    def test_initialization(self, response_generator):
        """Test l'initialisation de ChatResponseGenerator."""
        assert response_generator.llm_selector is not None

    @patch('app.src.ui.components.llm.llm_selector.LLMSelector.get_llm')
    def test_generate_response(self, mock_get_llm, response_generator, mock_document_reference):
        """Test la génération de réponse avec des segments."""
        # Préparation des données de test
        query = "Quelle est la capitale de la France?"
        segments = [
            mock_document_reference,
            mock_document_reference._replace(
                text="La France est un pays d'Europe.",
                relevance_score=0.7
            )
        ]

        # Configuration du mock LLM
        mock_llm = Mock()
        mock_llm.make_llm_call.return_value = "D'après [Source 1], Paris est la capitale de la France."
        mock_get_llm.return_value = mock_llm

        # Appel de la méthode à tester
        response = response_generator.generate_response(query, segments)

        # Vérifications
        assert response is not None
        mock_llm.make_llm_call.assert_called_once()
        
        # Vérification du contenu des messages envoyés au LLM
        call_args = mock_llm.make_llm_call.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[1]["role"] == "user"
        assert call_args[1]["content"] == query
        
        # Vérification que le système prompt contient les sources dans le bon ordre
        system_prompt = call_args[0]["content"]
        assert "[Source 1]" in system_prompt
        assert "[Source 2]" in system_prompt

    @patch('app.src.ui.components.llm.llm_selector.LLMSelector.get_llm')
    def test_generate_response_empty_segments(self, mock_get_llm, response_generator):
        """Test la génération de réponse avec des segments vides."""
        query = "Question test"
        segments = []

        mock_llm = Mock()
        mock_llm.make_llm_call.return_value = "Je ne trouve pas d'information pertinente dans les sources fournies."
        mock_get_llm.return_value = mock_llm

        response = response_generator.generate_response(query, segments)
        
        assert response is not None
        mock_llm.make_llm_call.assert_called_once()
