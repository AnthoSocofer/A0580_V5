import unittest
from unittest.mock import Mock, patch
from dataclasses import dataclass

@dataclass
class DocumentReference:
    text: str
    relevance_score: float
    title: str = ""
    pages: str = ""

from src.ui.components.chat.chat_response_generator import ChatResponseGenerator

class TestChatResponseGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.response_generator = ChatResponseGenerator()

    def test_initialization(self):
        """Test the initialization of ChatResponseGenerator"""
        self.assertIsNotNone(self.response_generator.llm_selector)

    @patch('src.ui.components.llm.llm_selector.LLMSelector.get_llm')
    def test_generate_response(self, mock_get_llm):
        """Test response generation with mock segments"""
        # Préparation des données de test
        query = "Quelle est la capitale de la France?"
        segments = [
            DocumentReference(text="Paris est la capitale de la France.", relevance_score=0.9),
            DocumentReference(text="La France est un pays d'Europe.", relevance_score=0.7)
        ]

        # Configuration du mock LLM
        mock_llm = Mock()
        mock_llm.make_llm_call.return_value = "D'après [Source 1], Paris est la capitale de la France."
        mock_get_llm.return_value = mock_llm

        # Appel de la méthode à tester
        response = self.response_generator.generate_response(query, segments)

        # Vérifications
        self.assertIsNotNone(response)
        mock_llm.make_llm_call.assert_called_once()
        
        # Vérification du contenu des messages envoyés au LLM
        call_args = mock_llm.make_llm_call.call_args[0][0]
        self.assertEqual(len(call_args), 2)
        self.assertEqual(call_args[1]["role"], "user")
        self.assertEqual(call_args[1]["content"], query)
        
        # Vérification que le système prompt contient les sources dans le bon ordre
        system_prompt = call_args[0]["content"]
        self.assertIn("[Source 1] Paris est la capitale de la France.", system_prompt)
        self.assertIn("[Source 2] La France est un pays d'Europe.", system_prompt)

    @patch('src.ui.components.llm.llm_selector.LLMSelector.get_llm')
    def test_generate_response_empty_segments(self, mock_get_llm):
        """Test response generation with empty segments"""
        query = "Question test"
        segments = []

        mock_llm = Mock()
        mock_llm.make_llm_call.return_value = "Je ne trouve pas d'information pertinente dans les sources fournies."
        mock_get_llm.return_value = mock_llm

        response = self.response_generator.generate_response(query, segments)
        
        self.assertIsNotNone(response)
        mock_llm.make_llm_call.assert_called_once()

if __name__ == '__main__':
    unittest.main()
