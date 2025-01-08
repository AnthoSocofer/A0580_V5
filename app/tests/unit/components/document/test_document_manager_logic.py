"""
Tests unitaires pour la logique de gestion des documents.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.pages.components.document.domain.document_manager_logic import DocumentManagerLogic
from src.pages.interfaces.document import IDocument

class TestDocumentManagerLogic:
    """Tests pour DocumentManagerLogic."""
    
    @pytest.fixture
    def mock_document(self):
        """Fixture pour le mock d'un document."""
        doc = Mock(spec=IDocument)
        doc.id = "doc1"
        doc.title = "Test Document"
        doc.metadata = {"kb_id": "kb1"}
        return doc
    
    @pytest.fixture
    def mock_state_manager(self):
        """Fixture pour le mock du gestionnaire d'état."""
        return Mock()
    
    @pytest.fixture
    def mock_document_processor(self):
        """Fixture pour le mock du processeur de documents."""
        processor = Mock()
        processor.process_document.return_value = Mock(spec=IDocument)
        return processor
    
    @pytest.fixture
    def mock_document_store(self):
        """Fixture pour le mock du stockage de documents."""
        store = Mock()
        store.save_document.return_value = "doc1"
        return store
    
    @pytest.fixture
    def mock_document_validator(self):
        """Fixture pour le mock du validateur de documents."""
        validator = Mock()
        validator.validate_file.return_value = True
        validator.get_supported_extensions.return_value = [".pdf", ".txt"]
        return validator
    
    @pytest.fixture
    def document_logic(self, mock_state_manager, mock_document_processor,
                      mock_document_store, mock_document_validator):
        """Fixture pour la logique de gestion des documents."""
        return DocumentManagerLogic(
            state_manager=mock_state_manager,
            document_processor=mock_document_processor,
            document_store=mock_document_store,
            document_validator=mock_document_validator
        )
    
    def test_upload_document_success(self, document_logic, mock_document_validator,
                                   mock_document_processor, mock_document_store):
        """Teste le téléchargement réussi d'un document."""
        mock_file = Mock()
        document_id = document_logic.upload_document(mock_file, "kb1")
        
        # Vérifie la validation
        mock_document_validator.validate_file.assert_called_once_with(mock_file)
        
        # Vérifie le traitement
        mock_document_processor.process_document.assert_called_once()
        
        # Vérifie la sauvegarde
        mock_document_store.save_document.assert_called_once()
        assert document_id == "doc1"
    
    def test_upload_document_invalid(self, document_logic, mock_document_validator):
        """Teste le téléchargement d'un document invalide."""
        mock_document_validator.validate_file.return_value = False
        mock_file = Mock()
        
        document_id = document_logic.upload_document(mock_file, "kb1")
        assert document_id is None
    
    def test_get_document(self, document_logic, mock_document_store, mock_document):
        """Teste la récupération d'un document."""
        mock_document_store.get_document.return_value = mock_document
        document = document_logic.get_document("doc1")
        
        mock_document_store.get_document.assert_called_once_with("doc1")
        assert document.id == "doc1"
    
    def test_list_documents(self, document_logic, mock_document_store, mock_document):
        """Teste la liste des documents."""
        mock_document_store.list_documents.return_value = [mock_document]
        documents = document_logic.list_documents("kb1")
        
        mock_document_store.list_documents.assert_called_once_with("kb1")
        assert len(documents) == 1
        assert documents[0].id == "doc1"
    
    def test_delete_document_success(self, document_logic, mock_document_store):
        """Teste la suppression réussie d'un document."""
        success = document_logic.delete_document("doc1")
        
        mock_document_store.delete_document.assert_called_once_with("doc1")
        assert success is True
    
    def test_delete_document_failure(self, document_logic, mock_document_store):
        """Teste l'échec de suppression d'un document."""
        mock_document_store.delete_document.side_effect = Exception()
        success = document_logic.delete_document("doc1")
        
        assert success is False
    
    def test_get_supported_extensions(self, document_logic, mock_document_validator):
        """Teste la récupération des extensions supportées."""
        extensions = document_logic.get_supported_extensions()
        
        mock_document_validator.get_supported_extensions.assert_called_once()
        assert extensions == [".pdf", ".txt"]
