"""
Interface pour le rendu des bases de connaissances.
"""
from abc import abstractmethod
from typing import List, Any, Optional
from src.ui.interfaces.renderers.base import IBaseRenderer
from src.ui.interfaces.renderers.form import IFormRenderer

class IKBRenderer(IBaseRenderer, IFormRenderer):
    """Interface pour le rendu des bases de connaissances."""
    
    @abstractmethod
    def render_file_uploader(self,
                           label: str,
                           key: Optional[str] = None,
                           accept_multiple_files: bool = False,
                           help: Optional[str] = None,
                           accepted_types: Optional[List[str]] = None) -> Any:
        """Affiche un uploader de fichiers."""
        pass
