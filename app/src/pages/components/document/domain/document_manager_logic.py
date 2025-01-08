"""
Logique métier pour la gestion des documents.
"""
from typing import List, Dict, Any, Optional, BinaryIO
from src.pages.interfaces.document import (
    IDocument,
    IDocumentProcessor,
    IDocumentStore,
    IDocumentValidator
)
from src.pages.interfaces.state_manager import IStateManager
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.pages.components.document.domain.document_validator import DocumentValidator
from src.pages.components.document.domain.document_processor import DocumentProcessor
from src.pages.components.document.domain.document_store import DocumentStore

class DocumentManagerLogic:
    """Logique métier pour la gestion des documents."""
    
    def __init__(self,
                 state_manager: Optional[IStateManager] = None,
                 document_processor: Optional[IDocumentProcessor] = None,
                 document_store: Optional[IDocumentStore] = None,
                 document_validator: Optional[IDocumentValidator] = None,
                 kb_manager: Optional[KnowledgeBasesManager] = None):
        """Initialise la logique de gestion des documents."""
        self.state_manager = state_manager or StateManager
        self.kb_manager = kb_manager
        
        # Initialiser les composants avec leurs implémentations par défaut
        self.document_validator = document_validator or DocumentValidator()
        self.document_processor = document_processor or DocumentProcessor()
        self.document_store = document_store or (DocumentStore(kb_manager) if kb_manager else None)
    
    def upload_document(self, file: BinaryIO, kb_id: str) -> Optional[str]:
        """Télécharge un document."""
        if not self.document_validator or not self.document_processor or not self.document_store:
            return None
            
        # Validation du fichier
        if not self.document_validator.validate_file(file):
            return None
        
        # Traitement du document
        metadata = {
            "kb_id": kb_id,
            "doc_id": file.name,
            "title": file.name
        }
        document = self.document_processor.process_document(file, metadata)
        
        # Sauvegarde du document
        return self.document_store.save_document(document)
    
    def get_document(self, document_id: str) -> Optional[IDocument]:
        """Récupère un document."""
        if not self.document_store:
            return None
        return self.document_store.get_document(document_id)
    
    def list_documents(self, kb_id: str) -> List[IDocument]:
        """Liste les documents d'une base de connaissances."""
        if not self.document_store:
            return []
        return self.document_store.list_documents(kb_id)
    
    def delete_document(self, document_id: str) -> bool:
        """Supprime un document."""
        if not self.document_store:
            return False
        try:
            self.document_store.delete_document(document_id)
            return True
        except Exception:
            return False
    
    def get_supported_extensions(self) -> List[str]:
        """Retourne les extensions supportées."""
        if not self.document_validator:
            return []
        return self.document_validator.get_supported_extensions()
