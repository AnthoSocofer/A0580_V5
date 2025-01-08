"""
Composant d'affichage des documents.
"""
import streamlit as st
from typing import Optional, Dict, Any
from src.core.types import Document

class DocumentViewer:
    """Composant pour visualiser les documents."""
    
    def render_document(self, doc: Document) -> None:
        """Affiche un document.
        
        Args:
            doc: Document à afficher
        """
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"📄 **{doc.title or doc.filename}**")
            if doc.description:
                st.markdown(doc.description)
            if doc.page_count:
                st.markdown(f"Pages: {doc.page_count}")
            
        with col2:
            st.markdown(f"*{doc.filename}*")
    
    def render_document_reference(self, ref: Dict[str, Any]) -> None:
        """Affiche une référence à un document.
        
        Args:
            ref: Référence au document
        """
        st.markdown(f"📄 **{ref.get('title', ref.get('filename', 'Document sans titre'))}**")
        if ref.get('text'):
            st.markdown(ref['text'])
        if ref.get('page_numbers'):
            st.markdown(f"Pages: {ref['page_numbers'][0]}-{ref['page_numbers'][1]}")
        if ref.get('relevance_score'):
            st.markdown(f"Score: {ref['relevance_score']:.2f}")
