"""
Composants réutilisables pour la gestion des documents dans les bases de connaissances.
"""
import streamlit as st
import tempfile
from typing import List, Dict, Any, Callable, Optional
from src.core.state_manager import StateManager

def handle_document_operation(
    kb_id: str,
    operation_type: str,
    operation_callback: Callable,
    refresh_callback: Optional[Callable] = None
) -> None:
    """Gère une opération sur un document avec rafraîchissement de la vue.
    
    Args:
        kb_id: ID de la base de connaissances
        operation_type: Type d'opération ('add' ou 'delete')
        operation_callback: Callback effectuant l'opération
        refresh_callback: Callback optionnel pour rafraîchir la vue
    """
    try:
        # Exécuter l'opération
        operation_callback()
        
        # Message de succès selon le type d'opération
        if operation_type == 'add':
            st.success("Documents ajoutés avec succès!")
        elif operation_type == 'delete':
            st.success("Document supprimé avec succès!")
        
        # Rafraîchir la liste des documents dans la session
        kb_state = StateManager.get_kb_state()
        if 'knowledge_bases' in st.session_state:
            for kb in st.session_state.knowledge_bases:
                if kb['kb_id'] == kb_id:
                    # Forcer le rechargement des documents
                    kb['documents'] = None
                    break
        
        # Appeler le callback de rafraîchissement si fourni
        if refresh_callback:
            refresh_callback()
            
        # Forcer le rafraîchissement de l'interface
        st.rerun()
        
    except Exception as e:
        st.error(f"Erreur lors de l'opération: {str(e)}")

def handle_document_upload(
    kb_id: str,
    files: List[tempfile.NamedTemporaryFile],
    on_upload: Callable[[str, List[tempfile.NamedTemporaryFile]], None],
    refresh_callback: Optional[Callable] = None
) -> None:
    """Gère l'upload de documents avec rafraîchissement de la vue.
    
    Args:
        kb_id: ID de la base de connaissances
        files: Liste des fichiers à uploader
        on_upload: Callback d'upload des documents
        refresh_callback: Callback optionnel pour rafraîchir la vue
    """
    def upload_operation():
        on_upload(kb_id, files)
    
    handle_document_operation(
        kb_id=kb_id,
        operation_type='add',
        operation_callback=upload_operation,
        refresh_callback=refresh_callback
    )

def handle_document_delete(
    kb_id: str,
    doc_id: str,
    on_delete: Callable[[str, str], None],
    refresh_callback: Optional[Callable] = None
) -> None:
    """Gère la suppression d'un document avec rafraîchissement de la vue.
    
    Args:
        kb_id: ID de la base de connaissances
        doc_id: ID du document à supprimer
        on_delete: Callback de suppression du document
        refresh_callback: Callback optionnel pour rafraîchir la vue
    """
    def delete_operation():
        on_delete(kb_id, doc_id)
    
    handle_document_operation(
        kb_id=kb_id,
        operation_type='delete',
        operation_callback=delete_operation,
        refresh_callback=refresh_callback
    )
