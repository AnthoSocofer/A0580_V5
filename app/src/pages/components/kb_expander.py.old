"""
Composants d'interface pour les bases de connaissances.
"""
import streamlit as st
import tempfile
from typing import Dict, Any
from src.core.state_manager import StateManager
from src.pages.utils.kb_operations import KnowledgeBaseOperations
from src.pages.components.document_uploader import DocumentUploader
from src.core.types import KnowledgeBase, Document

class KnowledgeBaseCreator:
    """Composant pour la création d'une nouvelle base de connaissances."""
    
    def __init__(self, kb_operations: KnowledgeBaseOperations):
        """Initialise le créateur avec les opérations sur les bases."""
        self.kb_operations = kb_operations
    
    def render_form(self) -> None:
        """Affiche le formulaire de création d'une base."""
        with st.form("new_kb_form", clear_on_submit=True):
            kb_id = st.text_input(
                "ID de la base",
                placeholder="ma_base",
                help="Identifiant unique pour la base de connaissances"
            )
            kb_title = st.text_input(
                "Titre",
                placeholder="Ma Base de Connaissances",
                help="Titre descriptif de la base"
            )
            kb_description = st.text_area(
                "Description",
                placeholder="Description détaillée de la base...",
                help="Description du contenu et de l'usage de la base"
            )
            
            submit_button = st.form_submit_button("Créer")
            
            if submit_button:
                if not kb_id:
                    st.error("⚠️ L'ID de la base est requis!")
                elif not kb_title:
                    st.error("⚠️ Le titre de la base est requis!")
                else:
                    self.kb_operations.create_knowledge_base(kb_id, kb_title, kb_description)

class KnowledgeBaseExpander:
    """Composant pour l'affichage et la gestion d'une base de connaissances."""
    
    def __init__(self, kb_operations: KnowledgeBaseOperations):
        """Initialise l'expander avec les opérations sur les bases."""
        self.kb_operations = kb_operations
        self.document_uploader = DocumentUploader(kb_operations.kb_manager)
    
    def handle_expander_change(self, kb_id: str, is_expanded: bool) -> None:
        """Gère le changement d'état d'un expander."""
        kb_state = StateManager.get_kb_state()
        if is_expanded:
            if kb_state.active_expander != kb_id:
                kb_state.active_expander = kb_id
                StateManager.update_kb_state(kb_state)
                self.kb_operations.select_knowledge_base(kb_id)
        elif kb_state.active_expander == kb_id:
            kb_state.active_expander = None
            kb_state.current_kb = None
            kb_state.current_kb_id = None
            StateManager.update_kb_state(kb_state)
    
    def render_document_list(self, kb_id: str) -> None:
        """Affiche la liste des documents avec options de suppression."""
        st.markdown("#### Documents")
        documents = self.kb_operations.kb_manager.get_documents(kb_id)
        if not documents:
            st.info("Aucun document dans cette base")
        else:
            for doc in documents:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{doc.get('title', doc['doc_id'])}**")
                        if doc.get('description'):
                            st.caption(doc['description'])
                    with col2:
                        st.caption(f"Pages: {doc.get('page_count', '?')}")
                        if st.button("🗑️", key=f"delete_doc_{kb_id}_{doc['doc_id']}"):
                            self.document_uploader.handle_delete(kb_id, doc['doc_id'])
                st.divider()
    
    def render_delete_button(self, kb_id: str) -> None:
        """Affiche le bouton de suppression de la base."""
        st.markdown("---")
        if st.button("🗑️ Supprimer la base", type="primary", key=f"delete_kb_{kb_id}"):
            if st.button("⚠️ Confirmer la suppression", key=f"confirm_delete_kb_{kb_id}"):
                self.kb_operations.delete_knowledge_base(kb_id)
    
    def render_expander(self, kb: KnowledgeBase, is_active: bool) -> None:
        """Affiche l'expander complet pour une base de connaissances."""
        kb_id = kb['kb_id']
        unique_title = f"{kb.get('title', kb_id)} ({kb_id})"
        expander = st.expander(unique_title, expanded=is_active)
        
        with expander:
            st.markdown(f"**ID**: {kb_id}")
            if kb.get('description'):
                st.markdown(f"**Description**: {kb['description']}")
            
            # Si l'expander change d'état
            if expander.expanded != is_active:
                self.handle_expander_change(kb_id, expander.expanded)
            
            # Afficher les fonctionnalités si l'expander est actif
            if expander.expanded:
                st.markdown("---")
                
                # Upload de documents
                self.document_uploader.render_uploader(kb_id)
                
                # Liste des documents
                self.render_document_list(kb_id)
                
                # Bouton de suppression
                self.render_delete_button(kb_id)
    
    def render_list(self) -> None:
        """Affiche la liste des bases de connaissances."""
        kb_state = StateManager.get_kb_state()
        if not kb_state.knowledge_bases:
            st.warning("⚠️ Aucune base de connaissances disponible")
            return
            
        for kb in kb_state.knowledge_bases:
            self.render_expander(
                kb=kb,
                is_active=(kb['kb_id'] == kb_state.active_expander)
            )
