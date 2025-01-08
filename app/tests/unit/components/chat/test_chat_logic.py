"""
Tests unitaires pour la logique du chat.
"""
import pytest
from unittest.mock import Mock, patch

from app.src.ui.components.chat.business.chat_logic import ChatLogic
from app.src.ui.interfaces.state_manager import IStateManager
from app.src.ui.interfaces.chat import (
    IChatSourceManager,
    IChatResponseGenerator,
    IChatSearchManager
)

class TestChatLogic:
    """Tests pour ChatLogic."""
    
    @pytest.fixture
    def mock_state_manager(self):
        """Fixture pour le mock du gestionnaire d'état."""
        state_manager = Mock(spec=IStateManager)
        chat_state = ChatState()
        chat_state.messages = []
        chat_state.selected_kbs = ["kb1", "kb2"]
        state_manager.get_chat_state.return_value = chat_state
        return state_manager
    
    @pytest.fixture
    def mock_source_manager(self):
        """Fixture pour le mock du gestionnaire de sources."""
        return Mock(spec=IChatSourceManager)
    
    @pytest.fixture
    def mock_response_generator(self):
        """Fixture pour le mock du générateur de réponses."""
        generator = Mock(spec=IChatResponseGenerator)
        generator.generate_response.return_value = "Réponse test"
        return generator
    
    @pytest.fixture
    def mock_search_manager(self):
        """Fixture pour le mock du gestionnaire de recherche."""
        manager = Mock(spec=IChatSearchManager)
        manager.search_relevant_content.return_value = [
            {"title": "Doc1", "score": 0.8}
        ]
        return manager
    
    @pytest.fixture
    def chat_logic(self, mock_state_manager, mock_source_manager,
                  mock_response_generator, mock_search_manager):
        """Fixture pour la logique de chat."""
        return ChatLogic(
            state_manager=mock_state_manager,
            source_manager=mock_source_manager,
            response_generator=mock_response_generator,
            search_manager=mock_search_manager
        )
    
    def test_get_messages(self, chat_logic, mock_state_manager):
        """Teste la récupération des messages."""
        messages = chat_logic.get_messages()
        assert isinstance(messages, list)
        assert len(messages) == 0
    
    def test_add_user_message(self, chat_logic, mock_state_manager):
        """Teste l'ajout d'un message utilisateur."""
        chat_logic.add_user_message("Test message")
        
        # Vérifie que l'état a été mis à jour
        mock_state_manager.update_chat_state.assert_called_once()
        updated_state = mock_state_manager.update_chat_state.call_args[0][0]
        assert len(updated_state.messages) == 1
        assert updated_state.messages[0]["role"] == "user"
        assert updated_state.messages[0]["content"] == "Test message"
    
    def test_add_assistant_message(self, chat_logic, mock_state_manager):
        """Teste l'ajout d'un message assistant."""
        sources = [{"title": "Doc1", "score": 0.8}]
        chat_logic.add_assistant_message("Test response", sources)
        
        # Vérifie que l'état a été mis à jour
        mock_state_manager.update_chat_state.assert_called_once()
        updated_state = mock_state_manager.update_chat_state.call_args[0][0]
        assert len(updated_state.messages) == 1
        assert updated_state.messages[0]["role"] == "assistant"
        assert updated_state.messages[0]["content"] == "Test response"
        assert updated_state.messages[0]["sources"] == sources
    
    def test_generate_response(self, chat_logic, mock_search_manager,
                             mock_response_generator):
        """Teste la génération de réponse."""
        response, sources = chat_logic.generate_response("Test query")
        
        # Vérifie que la recherche a été effectuée
        mock_search_manager.search_relevant_content.assert_called_once_with(
            "Test query",
            ["kb1", "kb2"]
        )
        
        # Vérifie que la réponse a été générée
        mock_response_generator.generate_response.assert_called_once()
        assert response == "Réponse test"
        assert sources == [{"title": "Doc1", "score": 0.8}]
    
    def test_has_selected_kbs(self, chat_logic):
        """Teste la vérification des bases sélectionnées."""
        assert chat_logic.has_selected_kbs() is True

    def test_initialization(self, chat_logic):
        """Test l'initialisation de ChatLogic."""
        assert chat_logic.state_manager is not None
        assert chat_logic.source_manager is not None
        assert chat_logic.response_generator is not None
        assert chat_logic.search_manager is not None
