"""
Tests unitaires pour la logique de gestion des bases de connaissances.
"""
import pytest
from unittest.mock import Mock
from src.pages.components.kb.domain.kb_manager_logic import KBManagerLogic
from src.core.types import KnowledgeBase

class TestKBManagerLogic:
    """Tests pour KBManagerLogic."""
    
    @pytest.fixture
    def mock_kb(self):
        """Fixture pour le mock d'une base de connaissances."""
        kb = Mock(spec=KnowledgeBase)
        kb.id = "kb1"
        kb.title = "Test KB"
        kb.description = "Test Description"
        return kb
    
    @pytest.fixture
    def mock_state_manager(self):
        """Fixture pour le mock du gestionnaire d'état."""
        return Mock()
    
    @pytest.fixture
    def mock_kb_processor(self):
        """Fixture pour le mock du processeur de bases."""
        processor = Mock()
        processor.create_knowledge_base.return_value = Mock(spec=KnowledgeBase)
        return processor
    
    @pytest.fixture
    def mock_kb_store(self):
        """Fixture pour le mock du stockage de bases."""
        store = Mock()
        store.save_knowledge_base.return_value = "kb1"
        return store
    
    @pytest.fixture
    def mock_kb_validator(self):
        """Fixture pour le mock du validateur de bases."""
        validator = Mock()
        validator.validate_title.return_value = True
        validator.validate_description.return_value = True
        validator.validate_knowledge_base.return_value = True
        return validator
    
    @pytest.fixture
    def kb_logic(self, mock_state_manager, mock_kb_processor,
                 mock_kb_store, mock_kb_validator):
        """Fixture pour la logique de gestion des bases."""
        return KBManagerLogic(
            state_manager=mock_state_manager,
            kb_processor=mock_kb_processor,
            kb_store=mock_kb_store,
            kb_validator=mock_kb_validator
        )
    
    def test_create_kb_success(self, kb_logic, mock_kb_validator,
                             mock_kb_processor, mock_kb_store):
        """Teste la création réussie d'une base."""
        kb_id = kb_logic.create_knowledge_base("Test KB", "Test Description")
        
        # Vérifie la validation
        mock_kb_validator.validate_title.assert_called_once_with("Test KB")
        mock_kb_validator.validate_description.assert_called_once_with("Test Description")
        
        # Vérifie le traitement
        mock_kb_processor.create_knowledge_base.assert_called_once_with(
            "Test KB", "Test Description"
        )
        
        # Vérifie la sauvegarde
        mock_kb_store.save_knowledge_base.assert_called_once()
        assert kb_id == "kb1"
    
    def test_create_kb_invalid_title(self, kb_logic, mock_kb_validator):
        """Teste la création avec un titre invalide."""
        mock_kb_validator.validate_title.return_value = False
        
        kb_id = kb_logic.create_knowledge_base("Invalid", "Test Description")
        assert kb_id is None
    
    def test_update_kb_success(self, kb_logic, mock_kb_validator,
                             mock_kb_processor):
        """Teste la mise à jour réussie d'une base."""
        success = kb_logic.update_knowledge_base(
            "kb1", "New Title", "New Description"
        )
        
        # Vérifie la validation
        mock_kb_validator.validate_title.assert_called_once_with("New Title")
        mock_kb_validator.validate_description.assert_called_once_with("New Description")
        
        # Vérifie le traitement
        mock_kb_processor.update_knowledge_base.assert_called_once_with(
            "kb1", "New Title", "New Description"
        )
        
        assert success is True
    
    def test_delete_kb_success(self, kb_logic, mock_kb_processor,
                             mock_kb_store):
        """Teste la suppression réussie d'une base."""
        mock_kb_processor.delete_knowledge_base.return_value = True
        
        success = kb_logic.delete_knowledge_base("kb1")
        
        # Vérifie la suppression
        mock_kb_processor.delete_knowledge_base.assert_called_once_with("kb1")
        mock_kb_store.delete_knowledge_base.assert_called_once_with("kb1")
        
        assert success is True
    
    def test_list_kbs(self, kb_logic, mock_kb_store, mock_kb):
        """Teste la liste des bases."""
        mock_kb_store.list_knowledge_bases.return_value = [mock_kb]
        
        kbs = kb_logic.list_knowledge_bases()
        
        mock_kb_store.list_knowledge_bases.assert_called_once()
        assert len(kbs) == 1
        assert kbs[0].id == "kb1"
    
    def test_get_kb(self, kb_logic, mock_kb_store, mock_kb):
        """Teste la récupération d'une base."""
        mock_kb_store.get_knowledge_base.return_value = mock_kb
        
        kb = kb_logic.get_knowledge_base("kb1")
        
        mock_kb_store.get_knowledge_base.assert_called_once_with("kb1")
        assert kb.id == "kb1"
