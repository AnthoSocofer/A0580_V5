"""
Tests unitaires pour l'interface utilisateur de gestion des documents.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.pages.components.document.presentation.document_manager_ui import DocumentManagerUI
from src.pages.components.document.domain.document_manager_logic import DocumentManagerLogic
from src.pages.interfaces.document import IDocument

class TestDocumentManagerUI:
    """Tests pour DocumentManagerUI."""
    
    @pytest.fixture
    def mock_document(self):
        """Fixture pour le mock d'un document."""
        doc = Mock(spec=IDocument)
        doc.id = "doc1"
        doc.title = "Test Document"
        doc.metadata = {"kb_id": "kb1"}
        return doc
    
    @pytest.fixture
    def mock_document_logic(self, mock_document):
        """Fixture pour le mock de la logique de gestion des documents."""
        logic = Mock(spec=DocumentManagerLogic)
        logic.get_supported_extensions.return_value = [".pdf", ".txt"]
        logic.list_documents.return_value = [mock_document]
        logic.upload_document.return_value = "doc1"
        logic.delete_document.return_value = True
        return logic
    
    @pytest.fixture
    def mock_ui_renderer(self):
        """Fixture pour le mock du rendu UI."""
        renderer = Mock()
        renderer.render_file_uploader.return_value = None
        renderer.expander = MagicMock()
        renderer.render_button.return_value = False
        return renderer
    
    @pytest.fixture
    def document_ui(self, mock_document_logic, mock_ui_renderer):
        """Fixture pour l'interface utilisateur."""
        return DocumentManagerUI(
            document_logic=mock_document_logic,
            ui_renderer=mock_ui_renderer
        )
    
    def test_render_initial_state(self, document_ui, mock_ui_renderer,
                                mock_document_logic):
        """Teste le rendu initial."""
        document_ui.render("kb1")
        
        # Vérifie l'affichage du titre
        mock_ui_renderer.render_markdown.assert_any_call("## 📄 Documents")
        
        # Vérifie l'affichage des extensions supportées
        mock_ui_renderer.render_info.assert_any_call(
            "Extensions supportées : .pdf, .txt"
        )
        
        # Vérifie l'uploader
        mock_ui_renderer.render_file_uploader.assert_called_once_with(
            "Télécharger un document",
            accepted_types=[".pdf", ".txt"]
        )
    
    def test_handle_file_upload_success(self, document_ui, mock_ui_renderer,
                                      mock_document_logic):
        """Teste le téléchargement réussi d'un fichier."""
        mock_file = Mock()
        mock_ui_renderer.render_file_uploader.return_value = mock_file
        
        document_ui.render("kb1")
        
        # Vérifie le téléchargement
        mock_document_logic.upload_document.assert_called_once_with(mock_file, "kb1")
        
        # Vérifie le message de succès
        mock_ui_renderer.render_success.assert_called_once_with(
            "Document téléchargé avec succès (ID: doc1)"
        )
    
    def test_handle_file_upload_failure(self, document_ui, mock_ui_renderer,
                                      mock_document_logic):
        """Teste l'échec du téléchargement d'un fichier."""
        mock_file = Mock()
        mock_ui_renderer.render_file_uploader.return_value = mock_file
        mock_document_logic.upload_document.return_value = None
        
        document_ui.render("kb1")
        
        # Vérifie le message d'erreur
        mock_ui_renderer.render_error.assert_called_once_with(
            "Erreur lors du téléchargement du document"
        )
    
    def test_render_document_list(self, document_ui, mock_ui_renderer,
                                mock_document_logic, mock_document):
        """Teste l'affichage de la liste des documents."""
        document_ui.render("kb1")
        
        # Vérifie l'affichage des documents
        mock_ui_renderer.expander.assert_called_once_with(
            "📄 Test Document",
            expanded=False
        )
    
    def test_delete_document_success(self, document_ui, mock_ui_renderer,
                                   mock_document_logic):
        """Teste la suppression réussie d'un document."""
        mock_ui_renderer.render_button.return_value = True
        
        document_ui.render("kb1")
        
        # Vérifie la suppression
        mock_document_logic.delete_document.assert_called_once_with("doc1")
        
        # Vérifie le message de succès
        mock_ui_renderer.render_success.assert_called_once_with("Document supprimé")
