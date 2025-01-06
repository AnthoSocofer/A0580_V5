"""
Page de gestion des bases de connaissances.
"""
import streamlit as st
import tempfile
import os
import logging
from typing import List
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from dsrag.knowledge_base import KnowledgeBase
from src.pages import components

class KnowledgeBasePage:
    """Page de gestion des bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise la page avec le gestionnaire de bases."""
        self.kb_manager = kb_manager
        self.logger = logging.getLogger(__name__)
        if 'current_kb' not in st.session_state:
            st.session_state.current_kb = None
        if 'active_expander' not in st.session_state:
            st.session_state.active_expander = None
        if 'current_kb_id' not in st.session_state:
            st.session_state.current_kb_id = None

    def handle_kb_creation(self, kb_id: str, title: str, description: str):
        """Gère la création d'une base de connaissances."""
        try:
            kb = self.kb_manager.create_knowledge_base(
                kb_id=kb_id,
                title=title,
                description=description,
                exists_ok=True
            )
            st.session_state.current_kb = kb
            st.session_state.current_kb_id = kb_id
            st.success(f"Base '{title}' créée avec succès!")
        except Exception as e:
            st.error(f"Erreur lors de la création: {str(e)}")
    
    def handle_kb_selection(self, kb_id: str):
        """Gère la sélection d'une base de connaissances."""
        if kb_id == st.session_state.get('current_kb_id'):  # Évite les rechargements inutiles
            return
            
        try:
            kb = self.kb_manager.get_knowledge_base(kb_id)
            if kb:
                st.session_state.current_kb = kb
                st.session_state.current_kb_id = kb_id
            else:
                st.error(f"Erreur lors du chargement de la base {kb_id}")
        except Exception as e:
            st.error(f"Erreur lors du chargement: {str(e)}")
    
    def handle_document_upload(self, files: List[tempfile.NamedTemporaryFile]):
        """Gère l'upload de documents."""
        kb = st.session_state.current_kb
        if not kb:
            st.error("Aucune base sélectionnée")
            return

        for uploaded_file in files:
            self.logger.info(f"Début du traitement du fichier: {uploaded_file.name}")
            self.logger.info(f"Ajout du document à la base {kb.kb_id}")
            
            # Créer un fichier temporaire pour stocker le contenu
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file.flush()
                
                try:
                    # Ajouter le document à la base
                    kb.add_document(
                        doc_id=uploaded_file.name,
                        file_path=tmp_file.name,
                        document_title=uploaded_file.name,
                        auto_context_config={
                            "use_generated_title": False,
                            "get_document_summary": True,
                            "get_section_summaries": True
                        }
                    )
                    
                    self.logger.info(f"Document {uploaded_file.name} ajouté avec succès à la base {kb.kb_id}")
                    st.success(f"Document {uploaded_file.name} ajouté avec succès!")
                    
                    # Marquer le fichier comme traité
                    upload_key = f"upload_{kb.kb_id}"
                    processed_key = f"processed_{upload_key}"
                    
                    if processed_key not in st.session_state:
                        st.session_state[processed_key] = set()
                    
                    st.session_state[processed_key].add(uploaded_file.name)
                    
                    # Forcer le rechargement de la liste des bases pour mettre à jour les documents
                    if 'knowledge_bases' in st.session_state:
                        del st.session_state.knowledge_bases
                    
                    # Recharger la page
                    st.rerun()
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'ajout du document {uploaded_file.name}: {str(e)}")
                    st.error(f"Erreur lors de l'ajout du document {uploaded_file.name}: {str(e)}")
                finally:
                    try:
                        # S'assurer que le fichier temporaire est fermé et supprimé
                        self.logger.debug(f"Nettoyage du fichier temporaire: {tmp_file.name}")
                        tmp_file.close()
                        os.unlink(tmp_file.name)
                        self.logger.debug("Fichier temporaire supprimé avec succès")
                    except Exception as e:
                        self.logger.error(f"Erreur lors de la suppression du fichier temporaire: {str(e)}")
    
    def handle_expander_change(self, kb_id: str, is_expanded: bool):
        """Gère le changement d'état d'un expander."""
        if is_expanded:
            if st.session_state.active_expander != kb_id:
                st.session_state.active_expander = kb_id
                self.handle_kb_selection(kb_id)
        elif st.session_state.active_expander == kb_id:
            st.session_state.active_expander = None
            st.session_state.current_kb = None
            st.session_state.current_kb_id = None
    
    def handle_document_delete(self, kb_id: str, doc_id: str):
        """Gère la suppression d'un document."""
        try:
            self.kb_manager.delete_document(kb_id, doc_id)
            st.success(f"Document {doc_id} supprimé")
            # Forcer le rechargement de la liste des bases pour mettre à jour les documents
            if 'knowledge_bases' in st.session_state:
                del st.session_state.knowledge_bases
            # Forcer le rechargement de la page
            st.rerun()
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {str(e)}")

    def handle_kb_delete(self, kb_id: str):
        """Gère la suppression d'une base de connaissances."""
        if self.kb_manager.delete_knowledge_base(kb_id):
            st.success(f"Base {kb_id} supprimée")
            st.session_state.active_expander = None
            st.session_state.current_kb = None
            st.session_state.current_kb_id = None
            if 'knowledge_bases' in st.session_state:
                st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
            st.rerun()

    def render(self):
        """Affiche la page de gestion des bases de connaissances."""
        
        st.title("Gestion des Bases de Connaissances")
        
        # Création d'une nouvelle base
        with st.expander("Créer une nouvelle base", expanded=False):
            components.create_knowledge_base_form(self.handle_kb_creation)
        
        # Bases disponibles
        st.markdown("### Bases disponibles")
        
        components.knowledge_bases_list(
            kb_manager=self.kb_manager,
            active_expander=st.session_state.active_expander,
            on_expander_change=self.handle_expander_change,
            on_document_upload=self.handle_document_upload,
            on_document_delete=self.handle_document_delete,
            on_kb_delete=self.handle_kb_delete
        )
