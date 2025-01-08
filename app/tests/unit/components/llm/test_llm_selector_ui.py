"""
Tests unitaires pour l'interface utilisateur de sélection LLM.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.pages.components.llm.presentation.llm_selector_ui import LLMSelectorUI
from src.pages.components.llm.domain.llm_selector_logic import LLMSelectorLogic

class TestLLMSelectorUI:
    """Tests pour LLMSelectorUI."""
    
    @pytest.fixture
    def mock_selector_logic(self):
        """Fixture pour le mock de la logique de sélection."""
        logic = Mock(spec=LLMSelectorLogic)
        logic.get_current_selection.return_value = {
            "provider": "OpenAI",
            "model": "3.5-turbo"
        }
        logic.get_providers.return_value = ["OpenAI", "Anthropic"]
        logic.get_models_for_provider.return_value = ["3.5-turbo", "4o"]
        return logic
    
    @pytest.fixture
    def mock_ui_renderer(self):
        """Fixture pour le mock du rendu UI."""
        renderer = Mock()
        renderer.render_select.return_value = "OpenAI"
        return renderer
    
    @pytest.fixture
    def selector_ui(self, mock_selector_logic, mock_ui_renderer):
        """Fixture pour l'interface utilisateur."""
        return LLMSelectorUI(
            selector_logic=mock_selector_logic,
            ui_renderer=mock_ui_renderer
        )
    
    def test_render(self, selector_ui, mock_selector_logic, mock_ui_renderer):
        """Teste le rendu de l'interface."""
        selector_ui.render()
        
        # Vérifie que les méthodes de rendu ont été appelées
        assert mock_ui_renderer.render_select.call_count == 2
        
        # Vérifie les appels pour le sélecteur de fournisseur
        provider_call = mock_ui_renderer.render_select.call_args_list[0]
        assert provider_call[1]["label"] == "Fournisseur LLM"
        assert provider_call[1]["options"] == ["OpenAI", "Anthropic"]
        
        # Vérifie les appels pour le sélecteur de modèle
        model_call = mock_ui_renderer.render_select.call_args_list[1]
        assert model_call[1]["label"] == "Modèle"
        assert model_call[1]["options"] == ["3.5-turbo", "4o"]
    
    def test_on_provider_change(self, selector_ui, mock_selector_logic):
        """Teste le changement de fournisseur."""
        mock_selector_logic.get_current_selection.return_value = {
            "provider": "Anthropic",
            "model": "invalid_model"
        }
        mock_selector_logic.get_models_for_provider.return_value = ["haiku", "opus"]
        
        selector_ui._on_provider_change()
        
        # Vérifie que la sélection a été mise à jour avec le premier modèle disponible
        mock_selector_logic.update_selection.assert_called_once_with("Anthropic", "haiku")
