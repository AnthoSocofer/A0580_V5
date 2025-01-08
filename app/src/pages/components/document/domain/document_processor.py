"""
Processeur de documents.
"""
from typing import Dict, Any, BinaryIO
from src.pages.interfaces.document import IDocumentProcessor, IDocument

class Document(IDocument):
    """Implémentation de l'interface IDocument."""
    
    def __init__(self, id: str, title: str, content: str, metadata: Dict[str, Any], kb_id: str):
        """Initialise un document."""
        self.id = id
        self.title = title
        self.content = content
        self.metadata = metadata
        self.kb_id = kb_id

class DocumentProcessor(IDocumentProcessor):
    """Processeur de documents."""
    
    def process_document(self, file: BinaryIO, metadata: Dict[str, Any]) -> IDocument:
        """Traite un document."""
        content = self.extract_text(file)
        doc_metadata = {**self.extract_metadata(file), **metadata}
        
        return Document(
            id=metadata.get('doc_id', ''),
            title=metadata.get('title', ''),
            content=content,
            metadata=doc_metadata,
            kb_id=metadata.get('kb_id', '')
        )
    
    def extract_text(self, file: BinaryIO) -> str:
        """Extrait le texte d'un document."""
        # Pour l'instant, on suppose que c'est un fichier texte
        return file.read().decode('utf-8')
    
    def extract_metadata(self, file: BinaryIO) -> Dict[str, Any]:
        """Extrait les métadonnées d'un document."""
        # Pour l'instant, on retourne juste le nom du fichier
        return {
            'filename': getattr(file, 'name', ''),
            'size': len(file.read())
        }
