"""
Tests unitaires pour l'interface utilisateur de filtrage des bases de connaissances.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.pages.components.filters.presentation.kb_filter_ui import KBFilterUI
from src.pages.components.filters.domain.kb_filter_logic import KBFilterLogic

class TestKBFilterUI:
    """Tests pour KBFilterUI."""
    
    @pytest.fixture
    def mock_filter_logic(self):
        """Fixture pour le mock de la logique de filtrage."""
        logic = Mock(spec=KBFilterLogic)
        logic.has_available_kbs.return_value = True
        logic.get_kb_options.return_value = {
            "Base 1 (kb1)": "kb1",
            "Base 2 (kb2)": "kb2",
            "Base 3 (kb3)": "kb3"
        }
        logic.get_selected_options.return_value = ["Base 1 (kb1)", "Base 2 (kb2)"]
        return logic
    
    @pytest.fixture
    def mock_ui_renderer(self):
        """Fixture pour le mock du rendu UI."""
        renderer = Mock()
        renderer.render_multiselect.return_value = ["Base 1 (kb1)", "Base 3 (kb3)"]
        return renderer
    
    @pytest.fixture
    def filter_ui(self, mock_filter_logic, mock_ui_renderer):
        """Fixture pour l'interface utilisateur."""
        return KBFilterUI(
            filter_logic=mock_filter_logic,
            ui_renderer=mock_ui_renderer
        )
    
    def test_render_with_available_kbs(self, filter_ui, mock_filter_logic, mock_ui_renderer):
        """Teste le rendu avec des bases disponibles."""
        filter_ui.render()
        
        # Vérifie que le multiselect a été rendu
        mock_ui_renderer.render_multiselect.assert_called_once()
        call_args = mock_ui_renderer.render_multiselect.call_args[1]
        assert call_args["label"] == "Bases de connaissances"
        assert set(call_args["options"]) == {"Base 1 (kb1)", "Base 2 (kb2)", "Base 3 (kb3)"}
        assert set(call_args["default"]) == {"Base 1 (kb1)", "Base 2 (kb2)"}
        
        # Vérifie que la sélection a été mise à jour
        mock_filter_logic.update_selected_kbs.assert_called_once_with(
            ["Base 1 (kb1)", "Base 3 (kb3)"]
        )
    
    def test_render_without_available_kbs(self, filter_ui, mock_filter_logic, mock_ui_renderer):
        """Teste le rendu sans bases disponibles."""
        mock_filter_logic.has_available_kbs.return_value = False
        filter_ui.render()
        
        # Vérifie que le message d'info a été affiché
        mock_ui_renderer.render_info.assert_called_once_with(
            "Aucune base de connaissances disponible."
        )
        
        # Vérifie que le multiselect n'a pas été rendu
        mock_ui_renderer.render_multiselect.assert_not_called()
