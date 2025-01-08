"""
Tests unitaires pour l'interface utilisateur du chat.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from app.src.ui.components.chat.view.chat_ui import ChatUI
from app.src.ui.components.chat.business.chat_logic import ChatLogic
from app.src.ui.interfaces.state_manager import IStateManager

class TestChatUI:
    """Tests pour ChatUI."""
    
    @pytest.fixture
    def mock_chat_logic(self):
        """Fixture pour le mock de la logique de chat."""
        logic = Mock(spec=ChatLogic)
        logic.has_selected_kbs.return_value = True
        logic.get_messages.return_value = [
            {
                "role": "user",
                "content": "Test message",
                "id": "msg_0"
            },
            {
                "role": "assistant",
                "content": "Test response",
                "sources": [{"title": "Doc1", "score": 0.8}],
                "id": "msg_1"
            }
        ]
        logic.generate_response.return_value = ("Test response", [{"title": "Doc1", "score": 0.8}])
        return logic
    
    @pytest.fixture
    def mock_ui_renderer(self):
        """Fixture pour le mock du rendu UI."""
        renderer = Mock()
        renderer.chat_message = MagicMock()
        renderer.expander = MagicMock()
        renderer.render_chat_input.return_value = "Test input"
        return renderer
    
    @pytest.fixture
    def chat_ui(self, mock_chat_logic, mock_ui_renderer):
        """Fixture pour l'interface utilisateur."""
        state_manager = Mock(spec=IStateManager)
        return ChatUI(
            chat_logic=mock_chat_logic,
            ui_renderer=mock_ui_renderer,
            state_manager=state_manager
        )
    
    def test_render_with_selected_kbs(self, chat_ui, mock_chat_logic, mock_ui_renderer):
        """Teste le rendu avec des bases sélectionnées."""
        chat_ui.render()
        
        # Vérifie l'affichage du titre
        mock_ui_renderer.render_markdown.assert_any_call("## 💬 Discussion")
        
        # Vérifie l'affichage des messages
        assert mock_ui_renderer.chat_message.call_count == 2
        
        # Vérifie la gestion de l'entrée utilisateur
        mock_ui_renderer.render_chat_input.assert_called_once_with("Votre message")
        mock_chat_logic.add_user_message.assert_called_once_with("Test input")
        mock_chat_logic.generate_response.assert_called_once_with("Test input")
        mock_chat_logic.add_assistant_message.assert_called_once_with(
            "Test response",
            [{"title": "Doc1", "score": 0.8}]
        )
    
    def test_render_without_selected_kbs(self, chat_ui, mock_chat_logic, mock_ui_renderer):
        """Teste le rendu sans bases sélectionnées."""
        mock_chat_logic.has_selected_kbs.return_value = False
        chat_ui.render()
        
        # Vérifie l'affichage du message d'info
        mock_ui_renderer.render_info.assert_called_once_with(
            "Sélectionnez au moins une base de connaissances dans la barre latérale pour commencer."
        )
        
        # Vérifie qu'aucun message n'est affiché
        mock_ui_renderer.chat_message.assert_not_called()
        mock_ui_renderer.render_chat_input.assert_not_called()

    def test_initialization(self, chat_ui):
        """Test l'initialisation de ChatUI."""
        assert chat_ui.chat_logic is not None
        assert chat_ui.state_manager is not None
