"""
Validateur de documents.
"""
import os
from typing import List, Any
from src.ui.interfaces.document import IDocumentValidator

class DocumentValidator(IDocumentValidator):
    """Validateur de documents."""
    
    def get_supported_extensions(self) -> List[str]:
        """Retourne les extensions supportées."""
        return [".pdf", ".txt", ".docx"]
    
    def validate_file(self, file: Any) -> bool:
        """Valide un fichier."""
        if not hasattr(file, 'name'):
            return False
            
        # Vérifier l'extension
        extension = os.path.splitext(file.name)[1].lower()
        return extension in self.get_supported_extensions()
