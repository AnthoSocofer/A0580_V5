"""
Composant pour l'upload et la gestion des documents.
"""
import streamlit as st
import tempfile
import os
import logging
from typing import List
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.types import Document, AutoContextConfig

class DocumentUploader:
    """Composant pour l'upload et la gestion des documents."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise l'uploader avec le gestionnaire de bases."""
        self.kb_manager = kb_manager
        self.logger = logging.getLogger(__name__)
    
    def handle_upload(self, files: List[tempfile.NamedTemporaryFile], kb_id: str) -> None:
        """Gère l'upload de documents."""
        if not kb_id:
            st.error("Aucune base sélectionnée")
            return

        upload_key = f"upload_{kb_id}"
        processed_key = f"processed_{upload_key}"
        
        if processed_key not in st.session_state:
            st.session_state[processed_key] = set()
            
        for uploaded_file in files:
            # Vérifier si le fichier a déjà été traité
            if uploaded_file.name in st.session_state[processed_key]:
                continue
                
            self.logger.info(f"Début du traitement du fichier: {uploaded_file.name}")
            self.logger.info(f"Ajout du document à la base {kb_id}")
            
            # Créer un fichier temporaire pour stocker le contenu
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                
                try:
                    # Ajouter le document à la base
                    self.kb_manager.add_document(
                        kb_id=kb_id,
                        doc_id=uploaded_file.name,
                        file_path=tmp_file.name,
                        document_title=uploaded_file.name,
                        auto_context_config={
                            "use_generated_title": False,
                            "get_document_summary": True,
                            "get_section_summaries": True
                        }
                    )
                    
                    self.logger.info(f"Document {uploaded_file.name} ajouté avec succès à la base {kb_id}")
                    st.success(f"Document {uploaded_file.name} ajouté avec succès!")
                    
                    # Marquer le fichier comme traité
                    st.session_state[processed_key].add(uploaded_file.name)
                    
                except Exception as e:
                    st.error(f"Erreur lors de l'ajout du document {uploaded_file.name}: {str(e)}")
                finally:
                    # Nettoyer le fichier temporaire
                    try:
                        os.unlink(tmp_file.name)
                    except:
                        pass
    
    def handle_delete(self, kb_id: str, doc_id: str) -> None:
        """Gère la suppression d'un document."""
        try:
            # Supprimer le document
            self.kb_manager.delete_document(kb_id, doc_id)
            
            # Mettre à jour l'état des bases
            kb_state = StateManager.get_kb_state()
            kb_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
            StateManager.update_kb_state(kb_state)
            
            # Forcer la mise à jour de l'interface
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {str(e)}")
    
    def render_uploader(self, kb_id: str) -> None:
        """Affiche l'interface d'upload de documents."""
        st.markdown("#### Ajouter des documents")
        
        # Clés uniques pour les widgets
        upload_key = f"upload_{kb_id}"
        state_key = f"upload_state_{kb_id}"
        
        # Initialiser l'état d'upload si nécessaire
        if state_key not in st.session_state:
            st.session_state[state_key] = {
                "pending_files": None,
                "upload_completed": False
            }
        
        upload_state = st.session_state[state_key]
        
        # Si l'upload est terminé, réinitialiser l'état
        if upload_state["upload_completed"]:
            upload_state["upload_completed"] = False
            upload_state["pending_files"] = None
        
        # Widget d'upload de fichiers
        uploaded_files = st.file_uploader(
            "Sélectionner des fichiers PDF",
            type=['pdf'],
            accept_multiple_files=True,
            key=upload_key
        )
        
        # Bouton de validation de l'upload
        if uploaded_files:
            # Ne mettre à jour l'état que si les fichiers ont changé
            if upload_state["pending_files"] != uploaded_files:
                upload_state["pending_files"] = uploaded_files
            
            if st.button("📤 Valider l'upload", key=f"validate_upload_{kb_id}"):
                self.handle_upload(upload_state["pending_files"], kb_id)
                upload_state["upload_completed"] = True
