"""
Interfaces pour la gestion des documents.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, BinaryIO

class IDocument:
    """Interface pour les documents."""
    id: str
    title: str
    content: str
    metadata: Dict[str, Any]
    kb_id: str

class IDocumentProcessor(ABC):
    """Interface pour le traitement des documents."""
    
    @abstractmethod
    def process_document(self, file: BinaryIO, metadata: Dict[str, Any]) -> IDocument:
        """Traite un document."""
        pass
    
    @abstractmethod
    def extract_text(self, file: BinaryIO) -> str:
        """Extrait le texte d'un document."""
        pass
    
    @abstractmethod
    def extract_metadata(self, file: BinaryIO) -> Dict[str, Any]:
        """Extrait les métadonnées d'un document."""
        pass

class IDocumentStore(ABC):
    """Interface pour le stockage des documents."""
    
    @abstractmethod
    def save_document(self, document: IDocument) -> str:
        """Sauvegarde un document."""
        pass
    
    @abstractmethod
    def get_document(self, document_id: str) -> Optional[IDocument]:
        """Récupère un document."""
        pass
    
    @abstractmethod
    def list_documents(self, kb_id: str) -> List[IDocument]:
        """Liste les documents d'une base de connaissances."""
        pass
    
    @abstractmethod
    def delete_document(self, document_id: str) -> None:
        """Supprime un document."""
        pass

class IDocumentValidator(ABC):
    """Interface pour la validation des documents."""
    
    @abstractmethod
    def validate_file(self, file: BinaryIO) -> bool:
        """Valide un fichier."""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Retourne les extensions supportées."""
        pass
