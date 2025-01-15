"""
Interface principale pour la gestion des bases de connaissances.
"""
import streamlit as st
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.pages.components.kb.kb_operations import KBOperations
from src.pages.components.kb.kb_creator import KBCreator
from src.pages.components.document.document_uploader import DocumentUploader

class KBInterface:
    """Interface principale pour la gestion des bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise l'interface.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_operations = KBOperations(kb_manager)
        self.kb_creator = KBCreator(self.kb_operations)
        self.document_uploader = DocumentUploader(kb_manager)
    
    def render(self):
        """Affiche l'interface de gestion des bases."""
        # Expander pour la création d'une nouvelle base
        with st.expander("➕ Nouvelle base", expanded=st.session_state.get('show_kb_form', False)):
            self.kb_creator.render_form()
        
        # Liste des bases existantes
        knowledge_bases = self.kb_operations.get_knowledge_bases()
        if knowledge_bases:
            for kb in knowledge_bases:
                kb_id = kb['kb_id']
                with st.expander(f"📚 {kb.get('title', kb_id)}", expanded=kb_id == st.session_state.get('active_kb')):
                    # Description
                    if kb.get('description'):
                        st.markdown(f"**Description**: {kb['description']}")
                    
                    # Upload de documents
                    st.markdown("### Ajouter des documents")
                    self.document_uploader.render_upload_form(kb_id)
                    
                    # Liste des documents
                    st.markdown("### Documents")
                    if kb.get('documents'):
                        for doc in kb['documents']:
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.markdown(f"📄 {doc.get('title', doc['doc_id'])}")
                            with col2:
                                if st.button("🗑️", key=f"delete_doc_{kb_id}_{doc['doc_id']}"):
                                    self.kb_operations.delete_document(kb_id, doc['doc_id'])
                                    st.rerun()
                    else:
                        st.info("Aucun document dans cette base")
                    
                    # Bouton de suppression de la base
                    st.markdown("---")
                    _, col2, _ = st.columns([1, 2, 1])
                    with col2:
                        if st.button("🗑️ Supprimer base de connaissances", key=f"delete_kb_{kb_id}"):
                            self.kb_operations.delete_knowledge_base(kb_id)
                            st.rerun()
        else:
            st.info("Aucune base de connaissances. Créez-en une pour commencer!")
