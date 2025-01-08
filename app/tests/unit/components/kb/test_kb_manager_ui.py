"""
Tests unitaires pour l'interface utilisateur de gestion des bases de connaissances.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.pages.components.kb.presentation.kb_manager_ui import KBManagerUI
from src.pages.components.kb.domain.kb_manager_logic import KBManagerLogic
from src.core.types import KnowledgeBase

class TestKBManagerUI:
    """Tests pour KBManagerUI."""
    
    @pytest.fixture
    def mock_kb(self):
        """Fixture pour le mock d'une base de connaissances."""
        kb = Mock(spec=KnowledgeBase)
        kb.id = "kb1"
        kb.title = "Test KB"
        kb.description = "Test Description"
        return kb
    
    @pytest.fixture
    def mock_kb_logic(self, mock_kb):
        """Fixture pour le mock de la logique de gestion des bases."""
        logic = Mock(spec=KBManagerLogic)
        logic.list_knowledge_bases.return_value = [mock_kb]
        logic.create_knowledge_base.return_value = "kb1"
        logic.update_knowledge_base.return_value = True
        logic.delete_knowledge_base.return_value = True
        return logic
    
    @pytest.fixture
    def mock_ui_renderer(self):
        """Fixture pour le mock du rendu UI."""
        renderer = Mock()
        renderer.expander = MagicMock()
        renderer.columns.return_value = [MagicMock(), MagicMock()]
        renderer.render_text_input.return_value = ""
        renderer.render_text_area.return_value = ""
        renderer.render_button.return_value = False
        return renderer
    
    @pytest.fixture
    def kb_ui(self, mock_kb_logic, mock_ui_renderer):
        """Fixture pour l'interface utilisateur."""
        return KBManagerUI(
            kb_logic=mock_kb_logic,
            ui_renderer=mock_ui_renderer
        )
    
    def test_render_initial_state(self, kb_ui, mock_ui_renderer):
        """Teste le rendu initial."""
        kb_ui.render()
        
        # Vérifie l'affichage du titre
        mock_ui_renderer.render_markdown.assert_any_call("## 📚 Bases de connaissances")
        
        # Vérifie l'expander de création
        mock_ui_renderer.expander.assert_any_call(
            "➕ Créer une nouvelle base",
            expanded=False
        )
    
    def test_create_kb_success(self, kb_ui, mock_ui_renderer, mock_kb_logic):
        """Teste la création réussie d'une base."""
        mock_ui_renderer.render_text_input.return_value = "New KB"
        mock_ui_renderer.render_text_area.return_value = "New Description"
        mock_ui_renderer.render_button.return_value = True
        
        kb_ui.render()
        
        # Vérifie la création
        mock_kb_logic.create_knowledge_base.assert_called_once_with(
            "New KB", "New Description"
        )
        
        # Vérifie le message de succès
        mock_ui_renderer.render_success.assert_called_once_with(
            "Base de connaissances créée avec succès (ID: kb1)"
        )
    
    def test_create_kb_missing_fields(self, kb_ui, mock_ui_renderer):
        """Teste la création avec des champs manquants."""
        mock_ui_renderer.render_text_input.return_value = ""
        mock_ui_renderer.render_text_area.return_value = ""
        mock_ui_renderer.render_button.return_value = True
        
        kb_ui.render()
        
        # Vérifie le message d'erreur
        mock_ui_renderer.render_error.assert_called_once_with(
            "Le titre et la description sont requis"
        )
    
    def test_update_kb_success(self, kb_ui, mock_ui_renderer, mock_kb_logic):
        """Teste la mise à jour réussie d'une base."""
        mock_ui_renderer.render_text_input.return_value = "Updated KB"
        mock_ui_renderer.render_text_area.return_value = "Updated Description"
        
        # Simule le clic sur le bouton de mise à jour
        def button_side_effect(label):
            return label == "💾 Mettre à jour"
        mock_ui_renderer.render_button.side_effect = button_side_effect
        
        kb_ui.render()
        
        # Vérifie la mise à jour
        mock_kb_logic.update_knowledge_base.assert_called_once_with(
            "kb1", "Updated KB", "Updated Description"
        )
        
        # Vérifie le message de succès
        mock_ui_renderer.render_success.assert_called_once_with("Base mise à jour")
    
    def test_delete_kb_success(self, kb_ui, mock_ui_renderer, mock_kb_logic):
        """Teste la suppression réussie d'une base."""
        # Simule le clic sur le bouton de suppression
        def button_side_effect(label):
            return label == "🗑️ Supprimer"
        mock_ui_renderer.render_button.side_effect = button_side_effect
        
        kb_ui.render()
        
        # Vérifie la suppression
        mock_kb_logic.delete_knowledge_base.assert_called_once_with("kb1")
        
        # Vérifie le message de succès
        mock_ui_renderer.render_success.assert_called_once_with("Base supprimée")
