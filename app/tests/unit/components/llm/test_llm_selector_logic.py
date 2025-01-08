"""
Tests unitaires pour la logique de sélection LLM.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.pages.components.llm.domain.llm_selector_logic import LLMSelectorLogic
from src.pages.states.llm_state import LLMState

class TestLLMSelectorLogic:
    """Tests pour LLMSelectorLogic."""
    
    @pytest.fixture
    def mock_state_manager(self):
        """Fixture pour le mock du gestionnaire d'état."""
        state_manager = Mock()
        llm_state = LLMState()
        llm_state.selected_llm = "OpenAI"
        llm_state.selected_model = "3.5-turbo"
        state_manager.get_llm_state.return_value = llm_state
        return state_manager
    
    @pytest.fixture
    def selector_logic(self, mock_state_manager):
        """Fixture pour la logique de sélection."""
        return LLMSelectorLogic(state_manager=mock_state_manager)
    
    def test_get_providers(self, selector_logic):
        """Teste la récupération des fournisseurs."""
        providers = selector_logic.get_providers()
        assert "OpenAI" in providers
        assert "Anthropic" in providers
        assert len(providers) == 2
    
    def test_get_models_for_provider(self, selector_logic):
        """Teste la récupération des modèles par fournisseur."""
        openai_models = selector_logic.get_models_for_provider("OpenAI")
        assert "3.5-turbo" in openai_models
        assert "4o" in openai_models
        
        anthropic_models = selector_logic.get_models_for_provider("Anthropic")
        assert "haiku" in anthropic_models
        assert "opus" in anthropic_models
    
    def test_get_model_id(self, selector_logic):
        """Teste la récupération des IDs de modèles."""
        assert selector_logic.get_model_id("OpenAI", "3.5-turbo") == "gpt-3.5-turbo"
        assert selector_logic.get_model_id("Anthropic", "haiku") == "claude-3-haiku-20240307"
    
    def test_get_current_selection(self, selector_logic, mock_state_manager):
        """Teste la récupération de la sélection actuelle."""
        selection = selector_logic.get_current_selection()
        assert selection["provider"] == "OpenAI"
        assert selection["model"] == "3.5-turbo"
    
    def test_update_selection(self, selector_logic, mock_state_manager):
        """Teste la mise à jour de la sélection."""
        selector_logic.update_selection("Anthropic", "haiku")
        
        # Vérifie que l'état a été mis à jour
        mock_state_manager.update_llm_state.assert_called_once()
        updated_state = mock_state_manager.update_llm_state.call_args[0][0]
        assert updated_state.selected_llm == "Anthropic"
        assert updated_state.selected_model == "haiku"
