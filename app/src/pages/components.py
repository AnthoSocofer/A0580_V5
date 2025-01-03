"""
Composants réutilisables pour l'interface utilisateur.
"""
import streamlit as st
import tempfile
from typing import List, Dict, Any, Callable, Optional

def create_knowledge_base_form(on_submit: Callable[[str, str, str], None]):
    """Formulaire de création d'une base de connaissances.
    
    Args:
        on_submit: Callback appelé lors de la soumission avec (kb_id, title, description)
    """
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
                on_submit(kb_id, kb_title, kb_description)

def knowledge_base_selector(
    knowledge_bases: List[Dict[str, Any]],
    current_kb_id: Optional[str],
    on_select: Callable[[str], None]
):
    """Sélecteur de base de connaissances.
    
    Args:
        knowledge_bases: Liste des bases disponibles
        current_kb_id: ID de la base actuellement sélectionnée
        on_select: Callback appelé lors de la sélection avec l'ID de la base
    """
    if not knowledge_bases:
        st.warning("⚠️ Aucune base de connaissances disponible")
        return
    
    # Création des colonnes pour chaque base
    for kb in knowledge_bases:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(
                f"📚 {kb['title'] or kb['kb_id']}",
                key=f"select_{kb['kb_id']}",
                help=kb['description'] or "Aucune description",
                type="primary" if kb['kb_id'] == current_kb_id else "secondary"
            ):
                on_select(kb['kb_id'])
        with col2:
            st.caption(f"{kb['document_count']} docs")
        
        if kb['description']:
            st.caption(kb['description'])
        st.divider()

def document_uploader(on_upload: Callable[[List[tempfile.NamedTemporaryFile]], None]):
    """Interface d'upload de documents.
    
    Args:
        on_upload: Callback appelé avec la liste des fichiers uploadés
    """
    uploaded_files = st.file_uploader(
        "Sélectionner des documents",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Formats acceptés: PDF, DOCX, TXT"
    )
    
    if uploaded_files:
        on_upload(uploaded_files)

def document_list(documents: List[Dict[str, Any]]):
    """Affichage de la liste des documents.
    
    Args:
        documents: Liste des documents à afficher
    """
    if not documents:
        st.info("Aucun document dans cette base")
        return
    
    for doc in documents:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{doc.get('title', doc['doc_id'])}**")
                if doc.get('description'):
                    st.caption(doc['description'])
            with col2:
                st.caption(f"Pages: {doc.get('page_count', '?')}")
        st.divider()
