"""
Tests unitaires pour la logique de filtrage des bases de connaissances.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.pages.components.filters.domain.kb_filter_logic import KBFilterLogic
from src.core.types import KnowledgeBase
from src.pages.states.chat_state import ChatState
from src.pages.states.kb_state import KBState

class TestKBFilterLogic:
    """Tests pour KBFilterLogic."""
    
    @pytest.fixture
    def mock_state_manager(self):
        """Fixture pour le mock du gestionnaire d'état."""
        state_manager = Mock()
        
        # Configuration de l'état du chat
        chat_state = ChatState()
        chat_state.selected_kbs = ["kb1", "kb2"]
        state_manager.get_chat_state.return_value = chat_state
        
        # Configuration de l'état des bases
        kb_state = KBState()
        kb_state.knowledge_bases = [
            KnowledgeBase(id="kb1", title="Base 1"),
            KnowledgeBase(id="kb2", title="Base 2"),
            KnowledgeBase(id="kb3", title="Base 3")
        ]
        state_manager.get_kb_state.return_value = kb_state
        
        return state_manager
    
    @pytest.fixture
    def filter_logic(self, mock_state_manager):
        """Fixture pour la logique de filtrage."""
        return KBFilterLogic(state_manager=mock_state_manager)
    
    def test_get_kb_options(self, filter_logic):
        """Teste la récupération des options de bases."""
        options = filter_logic.get_kb_options()
        assert len(options) == 3
        assert "Base 1 (kb1)" in options
        assert options["Base 1 (kb1)"] == "kb1"
    
    def test_get_selected_options(self, filter_logic):
        """Teste la récupération des options sélectionnées."""
        selected = filter_logic.get_selected_options()
        assert len(selected) == 2
        assert "Base 1 (kb1)" in selected
        assert "Base 2 (kb2)" in selected
    
    def test_update_selected_kbs(self, filter_logic, mock_state_manager):
        """Teste la mise à jour des bases sélectionnées."""
        new_selection = ["Base 1 (kb1)", "Base 3 (kb3)"]
        filter_logic.update_selected_kbs(new_selection)
        
        # Vérifie que l'état a été mis à jour
        mock_state_manager.update_chat_state.assert_called_once()
        updated_state = mock_state_manager.update_chat_state.call_args[0][0]
        assert set(updated_state.selected_kbs) == {"kb1", "kb3"}
    
    def test_has_available_kbs(self, filter_logic, mock_state_manager):
        """Teste la vérification de disponibilité des bases."""
        assert filter_logic.has_available_kbs() is True
        
        # Test avec aucune base
        kb_state = mock_state_manager.get_kb_state.return_value
        kb_state.knowledge_bases = []
        assert filter_logic.has_available_kbs() is False
