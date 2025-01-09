"""
Interface pour le rendu des documents.
"""
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Callable, BinaryIO, ContextManager

class IDocumentRenderer(ABC):
    """Interface pour le rendu des documents."""
    
    @abstractmethod
    def render_file_uploader(self,
                           label: str,
                           key: Optional[str] = None,
                           accept_multiple_files: bool = False,
                           help: Optional[str] = None,
                           accepted_types: Optional[List[str]] = None) -> Any:
        """Affiche un uploader de fichiers.
        
        Args:
            label: Label de l'uploader
            key: Clé unique pour l'uploader
            accept_multiple_files: Si True, permet l'upload de plusieurs fichiers
            help: Texte d'aide optionnel
            accepted_types: Liste des types de fichiers acceptés
            
        Returns:
            Le(s) fichier(s) uploadé(s)
        """
        pass
    
    @abstractmethod
    def render_document_info(self, document: Dict[str, Any]) -> None:
        """Affiche les informations d'un document.
        
        Args:
            document: Informations du document à afficher
        """
        pass
        
    @abstractmethod
    def render_document_list(self, documents: List[Dict[str, Any]]) -> None:
        """Affiche une liste de documents.
        
        Args:
            documents: Liste des documents à afficher
        """
        pass
    
    @abstractmethod
    def render_document_preview(self, content: str) -> None:
        """Affiche un aperçu du contenu d'un document.
        
        Args:
            content: Contenu du document à prévisualiser
        """
        pass
    
    @abstractmethod
    def render_document_metadata(self, metadata: Dict[str, Any]) -> None:
        """Affiche les métadonnées d'un document.
        
        Args:
            metadata: Métadonnées à afficher
        """
        pass
    
    @abstractmethod
    def render_document_actions(self, 
                              document_id: str,
                              on_delete: Optional[Callable[[str], None]] = None,
                              on_edit: Optional[Callable[[str], None]] = None) -> None:
        """Affiche les actions possibles sur un document.
        
        Args:
            document_id: ID du document
            on_delete: Callback pour la suppression
            on_edit: Callback pour l'édition
        """
        pass
