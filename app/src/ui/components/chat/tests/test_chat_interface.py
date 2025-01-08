import unittest
from unittest.mock import Mock, patch
import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))

from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.state_manager import StateManager
from src.ui.components.chat.chat_interface import ChatInterface

class TestChatInterface(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.kb_manager = Mock(spec=KnowledgeBasesManager)
        self.chat_interface = ChatInterface(self.kb_manager)

    @patch('streamlit.markdown')
    def test_initialization(self, mock_markdown):
        """Test the initialization of ChatInterface"""
        self.assertIsNotNone(self.chat_interface.source_manager)
        self.assertIsNotNone(self.chat_interface.response_generator)
        self.assertIsNotNone(self.chat_interface.search_manager)

    @patch('src.core.state_manager.StateManager.get_chat_state')
    @patch('src.core.state_manager.StateManager.get_kb_state')
    @patch('streamlit.info')
    def test_render_no_knowledge_bases(self, mock_info, mock_get_kb_state, mock_get_chat_state):
        """Test rendering when no knowledge bases are available"""
        mock_kb_state = Mock()
        mock_kb_state.knowledge_bases = []
        mock_get_kb_state.return_value = mock_kb_state
        
        self.chat_interface.render()
        mock_info.assert_called_once_with("Aucune base de connaissances n'est disponible.")

    @patch('src.core.state_manager.StateManager.get_chat_state')
    @patch('src.core.state_manager.StateManager.get_kb_state')
    @patch('streamlit.info')
    def test_render_no_selected_kbs(self, mock_info, mock_get_kb_state, mock_get_chat_state):
        """Test rendering when no knowledge bases are selected"""
        mock_kb_state = Mock()
        mock_kb_state.knowledge_bases = ['kb1']
        mock_get_kb_state.return_value = mock_kb_state
        
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = []
        mock_get_chat_state.return_value = mock_chat_state
        
        self.chat_interface.render()
        mock_info.assert_called_once_with("Sélectionnez au moins une base de connaissances dans la barre latérale pour commencer.")

    @patch('src.core.state_manager.StateManager.get_chat_state')
    @patch('src.core.state_manager.StateManager.get_kb_state')
    @patch('streamlit.chat_message')
    def test_render_messages(self, mock_chat_message, mock_get_kb_state, mock_get_chat_state):
        """Test rendering chat messages"""
        mock_kb_state = Mock()
        mock_kb_state.knowledge_bases = ['kb1']
        mock_get_kb_state.return_value = mock_kb_state
        
        mock_chat_state = Mock()
        mock_chat_state.selected_kbs = ['kb1']
        mock_chat_state.messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi", "sources": [{"title": "Doc1", "score": 0.9, "pages": "1-2"}]}
        ]
        mock_get_chat_state.return_value = mock_chat_state
        
        mock_message_container = Mock()
        mock_chat_message.return_value.__enter__.return_value = mock_message_container
        
        self.chat_interface.render()
        self.assertEqual(mock_chat_message.call_count, 2)

if __name__ == '__main__':
    unittest.main()
