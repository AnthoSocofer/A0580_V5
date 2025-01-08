"""
Logique métier pour l'upload de documents.
"""
from pathlib import Path
from typing import BinaryIO, Dict, Any
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class DocumentUploader:
    """Logique métier pour l'upload de documents."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise l'uploader.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
    
    def upload_document(self, kb_id: str, file: BinaryIO, filename: str) -> str:
        """Upload un document dans une base.
        
        Args:
            kb_id: ID de la base
            file: Fichier à uploader
            filename: Nom du fichier
            
        Returns:
            str: ID du document créé
            
        Raises:
            Exception: Si une erreur survient pendant l'upload
        """
        # Configuration par défaut pour le traitement automatique
        config = {
            "use_generated_title": False,
            "get_document_summary": True,
            "get_section_summaries": True
        }
        
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp_file:
            tmp_file.write(file.read())
            tmp_file.flush()
            
            try:
                # Ajouter le document
                doc_id = self.kb_manager.add_document(
                    kb_id=kb_id,
                    doc_id=filename,
                    file_path=tmp_file.name,
                    document_title=filename,
                    auto_context_config=config
                )
                
                return doc_id
                
            finally:
                # Supprimer le fichier temporaire
                if Path(tmp_file.name).exists():
                    Path(tmp_file.name).unlink()
