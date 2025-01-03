"""
Page de gestion des bases de connaissances.
"""
import streamlit as st
import tempfile
import os
from typing import List
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from dsrag.knowledge_base import KnowledgeBase
from src.pages import components

class KnowledgeBasePage:
    """Page de gestion des bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise la page avec le gestionnaire de bases."""
        self.kb_manager = kb_manager
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
        success = True
        for uploaded_file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
                
                try:
                    st.session_state.current_kb.add_document(
                        doc_id=uploaded_file.name,
                        file_path=tmp_path,
                        auto_context_config={
                            "use_generated_title": False,
                            "document_title": uploaded_file.name.replace('.pdf', '')
                        }
                    )
                    st.success(f"Document {uploaded_file.name} ajouté avec succès!")
                except Exception as e:
                    success = False
                    st.error(f"Erreur lors de l'ajout du document {uploaded_file.name}: {str(e)}")
                finally:
                    try:
                        os.unlink(tmp_path)
                    except Exception as e:
                        self.logger.warning(f"Erreur lors de la suppression du fichier temporaire: {str(e)}")
        
        if success:
            # Vider le cache du composant d'upload
            st.session_state[f"upload_{st.session_state.current_kb.kb_id}"] = None
            # Forcer le rechargement des bases
            if 'knowledge_bases' in st.session_state:
                st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
    
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
            # Forcer le rechargement des documents
            if 'knowledge_bases' in st.session_state:
                st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {str(e)}")

    def render(self):
        """Affiche la page de gestion des bases de connaissances."""
        st.title("Gestion des Bases de Connaissances")
        
        # Création d'une nouvelle base
        with st.expander("Créer une nouvelle base", expanded=False):
            components.create_knowledge_base_form(self.handle_kb_creation)
        
        # Bases disponibles
        st.markdown("### Bases disponibles")
        
        # Utiliser la liste des bases stockée dans la session
        if 'knowledge_bases' not in st.session_state:
            st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()

        for kb in st.session_state.knowledge_bases:
            kb_id = kb['kb_id']
            is_active = kb_id == st.session_state.active_expander
            
            # Utiliser un ID unique pour le titre de l'expander
            unique_title = f"{kb.get('title', kb_id)} ({kb_id})"
            expander = st.expander(unique_title, expanded=is_active)
            
            with expander:
                st.markdown(f"**ID**: {kb_id}")
                if kb.get('description'):
                    st.markdown(f"**Description**: {kb['description']}")
                st.markdown(f"**Documents**: {kb['document_count']}")

                # Si l'expander change d'état
                if expander.expanded != is_active:
                    self.handle_expander_change(kb_id, expander.expanded)
                    # st.rerun()  # Supprimé pour éviter les rechargements inutiles

                # Afficher les fonctionnalités si l'expander est actif
                if expander.expanded:
                    st.divider()
                    
                    # Composant d'upload de documents
                    uploaded_files = st.file_uploader(
                        "Ajouter des documents",
                        type=['pdf'],
                        accept_multiple_files=True,
                        help="Limite: 200MB par fichier • PDF",
                        key=f"upload_{kb_id}"
                    )
                    if uploaded_files:
                        self.handle_document_upload(uploaded_files)
                    
                    st.divider()
                    
                    # Afficher les documents
                    st.markdown("#### Documents disponibles")
                    try:
                        documents = self.kb_manager.list_documents(kb_id)
                        if documents:
                            # Créer des colonnes pour chaque ligne de document
                            for doc in documents:
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    doc_title = doc.get('title', doc['doc_id'])
                                    if isinstance(doc_title, dict) and 'title' in doc_title:
                                        doc_title = doc_title['title']
                                    st.text(doc_title)
                                with col2:
                                    if st.button("🗑️", key=f"delete_{kb_id}_{doc['doc_id']}"):
                                        self.handle_document_delete(kb_id, doc['doc_id'])
                        else:
                            st.info("Aucun document")
                    except Exception as e:
                        st.error(f"Erreur lors de la liste des documents: {str(e)}")
                    
                    st.divider()
                    
                    # Bouton de suppression
                    if st.button("🗑️ Supprimer la base", key=f"delete_{kb_id}", type="secondary"):
                        if self.kb_manager.delete_knowledge_base(kb_id):
                            st.success(f"Base {kb_id} supprimée")
                            st.session_state.active_expander = None
                            st.session_state.current_kb = None
                            st.session_state.current_kb_id = None
                            # st.rerun()  # Supprimé pour éviter les rechargements inutiles
