"""
Stockage de documents.
"""
from typing import List, Optional, Dict
from src.ui.interfaces.document import IDocumentStore, IDocument
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class DocumentStore(IDocumentStore):
    """Stockage de documents utilisant KnowledgeBasesManager."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise le stockage de documents."""
        self.kb_manager = kb_manager
        
    def save_document(self, document: IDocument) -> str:
        """Sauvegarde un document."""
        # Utiliser KnowledgeBasesManager pour sauvegarder le document
        success = self.kb_manager.add_document_content(
            kb_id=document.kb_id,
            doc_id=document.id,
            content=document.content,
            metadata=document.metadata
        )
        return document.id if success else ''
    
    def get_document(self, document_id: str) -> Optional[IDocument]:
        """Récupère un document."""
        # Pour l'instant, on ne peut pas récupérer un document spécifique
        return None
    
    def list_documents(self, kb_id: str) -> List[IDocument]:
        """Liste les documents d'une base de connaissances."""
        # Pour l'instant, on ne peut pas lister les documents
        return []
    
    def delete_document(self, document_id: str) -> None:
        """Supprime un document."""
        # Pour l'instant, on ne peut pas supprimer un document
        pass
