"""
Composant d'affichage des bases de connaissances.
"""
import streamlit as st
from typing import Optional
from src.core.types import KnowledgeBase
from src.pages.components.document.document_viewer import DocumentViewer
from src.pages.components.kb.kb_operations import KBOperations

class KBViewer:
    """Composant pour visualiser les bases de connaissances."""
    
    def __init__(self, kb_operations: KBOperations):
        """Initialise le composant.
        
        Args:
            kb_operations: Opérations sur les bases de connaissances
        """
        self.kb_operations = kb_operations
        self.document_viewer = DocumentViewer()
    
    def render_kb_details(self,
                         kb: KnowledgeBase,
                         expanded: bool = False) -> None:
        """Affiche les détails d'une base de connaissances.
        
        Args:
            kb: Base de connaissances à afficher
            expanded: Si True, l'expander sera ouvert par défaut
        """
        with st.expander(f"📚 {kb.title}", expanded=expanded):
            if kb.description:
                st.markdown(f"**Description**: {kb.description}")
            
            st.markdown(f"**Nombre de documents**: {len(kb.documents)}")
            
            # Affichage des documents
            if kb.documents:
                st.markdown("### Documents")
                for doc in kb.documents:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{doc.title or doc.filename}**")
                            if doc.description:
                                st.caption(doc.description)
                        with col2:
                            st.caption(f"*{doc.filename}*")
                            if st.button("🗑️", key=f"delete_doc_{doc.filename}"):
                                self.kb_operations.delete_document(kb.id, doc.filename)
                        st.divider()
            else:
                st.info("Aucun document dans cette base.")
