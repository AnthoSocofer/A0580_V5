"""
Composants réutilisables pour l'interface utilisateur.
"""
import streamlit as st
import tempfile
from typing import List, Dict, Any, Callable, Optional
from src.core.state_manager import StateManager
from src.pages.document_operations import handle_document_upload, handle_document_delete

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
    key = "document_uploader"
    uploaded_files = st.file_uploader(
        "Sélectionner des documents",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Formats acceptés: PDF, DOCX, TXT",
        key=key
    )
    
    if uploaded_files:
        # Process the upload
        on_upload(uploaded_files)
        
        # Clear the uploaded files from state
        kb_state = StateManager.get_kb_state()
        kb_state.uploaded_files = None
        StateManager.update_kb_state(kb_state)
        
        # Clear the file uploader
        st.session_state[key] = None
        st.rerun()

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

def knowledge_base_expander(
    kb: Dict[str, Any],
    is_active: bool,
    on_expander_change: Callable[[str, bool], None],
    on_document_upload: Callable[[List[tempfile.NamedTemporaryFile]], None],
    on_document_delete: Callable[[str, str], None],
    on_kb_delete: Callable[[str], None],
    kb_manager: Any
):
    """Affiche un expander pour une base de connaissances.
    
    Args:
        kb: Dictionnaire contenant les informations de la base
        is_active: Si l'expander est actuellement actif
        on_expander_change: Callback appelé lors du changement d'état de l'expander
        on_document_upload: Callback appelé lors de l'upload de documents
        on_document_delete: Callback appelé lors de la suppression d'un document
        on_kb_delete: Callback appelé lors de la suppression de la base
        kb_manager: Instance du gestionnaire de bases de connaissances
    """
    kb_id = kb['kb_id']
    unique_title = f"{kb.get('title', kb_id)} ({kb_id})"
    expander = st.expander(unique_title, expanded=is_active)
    
    with expander:
        st.markdown(f"**ID**: {kb_id}")
        if kb.get('description'):
            st.markdown(f"**Description**: {kb['description']}")
        
        # Si l'expander change d'état
        if expander.expanded != is_active:
            on_expander_change(kb_id, expander.expanded)
        
        # Afficher les fonctionnalités si l'expander est actif
        if expander.expanded:
            st.markdown("---")
            
            # Upload de documents
            st.markdown("#### Ajouter des documents")
            
            # Clé unique pour le widget d'upload
            upload_key = f"upload_{kb_id}"
            
            # Initialiser l'état d'upload si nécessaire
            if f"upload_state_{kb_id}" not in st.session_state:
                st.session_state[f"upload_state_{kb_id}"] = {
                    "pending_files": None,
                    "upload_completed": False
                }
            
            upload_state = st.session_state[f"upload_state_{kb_id}"]
            
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
                    upload_state["upload_completed"] = False
                
                if not upload_state["upload_completed"] and st.button("📤 Valider l'upload", key=f"validate_upload_{kb_id}"):
                    try:
                        # Appeler le callback d'upload
                        on_document_upload(upload_state["pending_files"])
                        st.success("Documents ajoutés avec succès!")
                        
                        # Marquer la base comme nécessitant un rafraîchissement
                        if 'knowledge_bases' in st.session_state:
                            for kb in st.session_state.knowledge_bases:
                                if kb['kb_id'] == kb_id:
                                    kb['documents'] = None
                                    break
                        
                        # Marquer l'upload comme terminé
                        upload_state["upload_completed"] = True
                        upload_state["pending_files"] = None
                        st.session_state[upload_key] = None
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Erreur lors de l'upload: {str(e)}")
                        upload_state["upload_completed"] = False
                        upload_state["pending_files"] = None
            
            # Liste des documents
            st.markdown("#### Documents disponibles")
            try:
                if 'documents' in kb:
                    documents = kb['documents']
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
                                button_key = f"delete_button_{kb_id}_{doc['doc_id']}"
                                
                                if st.button("🗑️", key=button_key):
                                    try:
                                        # Supprimer le document
                                        on_document_delete(kb_id, doc['doc_id'])
                                        st.success("Document supprimé avec succès!")
                                        
                                        # Marquer la base comme nécessitant un rafraîchissement
                                        if 'knowledge_bases' in st.session_state:
                                            for kb in st.session_state.knowledge_bases:
                                                if kb['kb_id'] == kb_id:
                                                    kb['documents'] = None
                                                    break
                                        
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Erreur lors de la suppression: {str(e)}")
                    else:
                        st.info("Aucun document dans cette base")
            except Exception as e:
                st.error(f"Erreur lors de l'affichage des documents: {str(e)}")
            
            # Bouton de suppression de la base
            st.markdown("---")
            if st.button("🗑️ Supprimer la base", key=f"delete_kb_{kb_id}", type="secondary"):
                if st.button("⚠️ Confirmer la suppression", key=f"confirm_delete_kb_{kb_id}", type="primary"):
                    on_kb_delete(kb_id)

def knowledge_bases_list(
    kb_manager: Any,
    active_expander: Optional[str],
    on_expander_change: Callable[[str, bool], None],
    on_document_upload: Callable[[List[tempfile.NamedTemporaryFile]], None],
    on_document_delete: Callable[[str, str], None],
    on_kb_delete: Callable[[str], None]
):
    """Affiche la liste des bases de connaissances.
    
    Args:
        kb_manager: Instance du gestionnaire de bases de connaissances
        active_expander: ID de l'expander actuellement actif
        on_expander_change: Callback appelé lors du changement d'état d'un expander
        on_document_upload: Callback appelé lors de l'upload de documents
        on_document_delete: Callback appelé lors de la suppression d'un document
        on_kb_delete: Callback appelé lors de la suppression de la base
    """
    # Utiliser la liste des bases depuis le state manager
    kb_state = StateManager.get_kb_state()
    
    # Vérifier si nous devons rafraîchir la liste des bases
    should_refresh = False
    if kb_state.knowledge_bases is None:
        should_refresh = True
    elif kb_state.knowledge_bases and any(kb.get('documents') is None for kb in kb_state.knowledge_bases):
        should_refresh = True
    
    # Charger ou rafraîchir la liste des bases si nécessaire
    if should_refresh:
        kb_state.knowledge_bases = kb_manager.list_knowledge_bases()
        StateManager.update_kb_state(kb_state)
    
    # S'assurer que knowledge_bases n'est pas None avant d'itérer
    if kb_state.knowledge_bases:
        for kb in kb_state.knowledge_bases:
            knowledge_base_expander(
                kb=kb,
                is_active=kb['kb_id'] == active_expander,
                on_expander_change=on_expander_change,
                on_document_upload=on_document_upload,
                on_document_delete=on_document_delete,
                on_kb_delete=on_kb_delete,
                kb_manager=kb_manager
            )
