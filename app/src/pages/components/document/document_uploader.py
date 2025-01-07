"""
Composant pour l'upload de documents.
"""
import streamlit as st
import tempfile
from pathlib import Path
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.types import AutoContextConfig

class DocumentUploader:
    """Composant pour l'upload de documents."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise l'uploader.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
    
    def render_upload_form(self, kb_id: str) -> None:
        """Affiche le formulaire d'upload de documents.
        
        Args:
            kb_id: Identifiant de la base de connaissances
        """
        uploaded_files = st.file_uploader(
            "Choisir des fichiers",
            accept_multiple_files=True,
            key=f"uploader_{kb_id}"
        )
        
        if uploaded_files:
            if st.button("Ajouter les documents"):
                with st.spinner("Traitement des documents..."):
                    for file in uploaded_files:
                        try:
                            # Créer un fichier temporaire
                            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.name).suffix) as tmp_file:
                                tmp_file.write(file.getvalue())
                                tmp_file.flush()
                                
                            # Configuration par défaut pour le traitement automatique
                            config = {
                                "use_generated_title": False,
                                "get_document_summary": True,
                                "get_section_summaries": True
                            }
                            
                            # Ajouter le document
                            self.kb_manager.add_document(
                                kb_id=kb_id,
                                doc_id=file.name,
                                file_path=tmp_file.name,
                                document_title=file.name,
                                auto_context_config=config
                            )
                            
                            # Supprimer le fichier temporaire
                            Path(tmp_file.name).unlink()
                            
                            st.success(f"Document '{file.name}' ajouté avec succès!")
                            
                        except Exception as e:
                            st.error(f"Erreur lors de l'ajout de '{file.name}': {str(e)}")
                            if Path(tmp_file.name).exists():
                                Path(tmp_file.name).unlink()
                
                # Recharger la page
                st.rerun()
