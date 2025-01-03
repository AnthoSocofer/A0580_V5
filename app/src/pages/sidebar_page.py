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
            st.success(f"Base '{title}' créée avec succès!")
        except Exception as e:
            st.error(f"Erreur lors de la création: {str(e)}")
    
    def handle_kb_selection(self, kb_id: str):
        """Gère la sélection d'une base de connaissances."""
        try:
            st.session_state.current_kb = self.kb_manager.get_knowledge_base(kb_id)
            if not st.session_state.current_kb:
                st.error(f"Erreur lors du chargement de la base {kb_id}")
        except Exception as e:
            st.error(f"Erreur lors du chargement: {str(e)}")
    
    def handle_document_upload(self, files: List[tempfile.NamedTemporaryFile]):
        """Gère l'upload de documents."""
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
                    st.success(f"Document {uploaded_file.name} ajouté!")
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
                finally:
                    os.unlink(tmp_path)
    
    def handle_expander_change(self, kb_id: str, is_expanded: bool):
        """Gère le changement d'état d'un expander."""
        if is_expanded:
            if st.session_state.active_expander != kb_id:
                st.session_state.active_expander = kb_id
                self.handle_kb_selection(kb_id)
        elif st.session_state.active_expander == kb_id:
            st.session_state.active_expander = None
            st.session_state.current_kb = None
    
    def render(self):
        """Affiche la page de gestion des bases de connaissances."""
        st.title("Gestion des Bases de Connaissances")
        
        # Création d'une nouvelle base
        with st.expander("Créer une nouvelle base", expanded=False):
            components.create_knowledge_base_form(self.handle_kb_creation)
        
        # Bases disponibles
        st.markdown("### Bases disponibles")
        if hasattr(st.session_state, 'knowledge_bases'):
            kb_list = st.session_state.knowledge_bases
        else:
            kb_list = self.kb_manager.list_knowledge_bases()
            st.session_state.knowledge_bases = kb_list

        for kb in kb_list:
            kb_id = kb['kb_id']
            is_active = kb_id == st.session_state.active_expander
            
            expander = st.expander(kb.get('title', kb_id), expanded=is_active)
            with expander:
                st.markdown(f"**ID**: {kb_id}")
                if kb.get('description'):
                    st.markdown(f"**Description**: {kb['description']}")
                st.markdown(f"**Documents**: {kb['document_count']}")

                # Si l'expander change d'état
                if expander.expanded != is_active:
                    self.handle_expander_change(kb_id, expander.expanded)
                    st.rerun()

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
                            with st.container():
                                doc_list = "\n".join([f"• {doc.get('title', doc['doc_id'])}" for doc in documents])
                                st.markdown(f"""
                                    <div style="max-height: 200px; overflow-y: auto;">
                                    {doc_list}
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("Aucun document dans cette base")
                    except Exception as e:
                        st.error(f"Erreur lors de la liste des documents: {str(e)}")
                    
                    st.divider()
                    
                    # Bouton de suppression
                    if st.button("🗑️ Supprimer la base", key=f"delete_{kb_id}", type="secondary"):
                        if self.kb_manager.delete_knowledge_base(kb_id):
                            st.success(f"Base {kb_id} supprimée")
                            st.session_state.active_expander = None
                            st.session_state.current_kb = None
                            st.rerun()
