"""
Filtre de documents pour la recherche.
"""
import streamlit as st
from typing import List, Dict, Any
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class DocumentFilter:
    """Filtre de documents pour la recherche."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise le filtre des documents.
        
        Args:
            kb_manager: Gestionnaire des bases de connaissances
        """
        self.kb_manager = kb_manager
        # Initialiser l'état du chat avec une liste vide de documents sélectionnés
        chat_state = StateManager.get_chat_state()
        if not hasattr(chat_state, 'selected_docs'):
            chat_state.selected_docs = []
        if not hasattr(chat_state, 'cached_documents'):
            chat_state.cached_documents = {}
        if not hasattr(chat_state, 'kb_options'):
            chat_state.kb_options = {}
        if not hasattr(chat_state, 'selected_kb_titles'):
            chat_state.selected_kb_titles = []
        if not hasattr(chat_state, 'kb_filter_initialized'):
            chat_state.kb_filter_initialized = False
        StateManager.update_chat_state(chat_state)
    
    def handle_kb_selection(self, selected_kbs: List[str]):
        """Gère la sélection des bases de connaissances.
        
        Args:
            selected_kbs: Liste des IDs des bases sélectionnées
        """
        chat_state = StateManager.get_chat_state()
        chat_state.selected_kbs = selected_kbs
        if not selected_kbs:  # Si aucune base sélectionnée, vider aussi la sélection des documents
            chat_state.selected_docs = []
        StateManager.update_chat_state(chat_state)
    
    def handle_doc_selection(self, selected_docs: List[str]):
        """Gère la sélection des documents.
        
        Args:
            selected_docs: Liste des IDs des documents sélectionnés
        """
        chat_state = StateManager.get_chat_state()
        chat_state.selected_docs = selected_docs
        StateManager.update_chat_state(chat_state)
    
    def render(self):
        """Affiche le filtre de documents."""
        chat_state = StateManager.get_chat_state()
        kb_state = StateManager.get_kb_state()
        
        # Initialiser ou mettre à jour le cache des documents
        if not chat_state.cached_documents:
            chat_state.cached_documents = {}
            for kb_id in chat_state.selected_kbs:
                if kb_id not in chat_state.cached_documents:
                    try:
                        kb = self.kb_manager.get_knowledge_base(kb_id)
                        if kb:
                            # Obtenir les IDs des documents depuis la base
                            doc_ids = kb.chunk_db.get_all_doc_ids()
                            # Créer les objets document
                            docs = [{"doc_id": doc_id} for doc_id in doc_ids]
                            chat_state.cached_documents[kb_id] = docs
                    except Exception as e:
                        st.error(f"Erreur lors de la récupération des documents de {kb_id}: {str(e)}")
            StateManager.update_chat_state(chat_state)
        
        # Construire la liste des documents disponibles
        all_docs = []
        for kb_id in chat_state.selected_kbs:
            docs = chat_state.cached_documents.get(kb_id, [])
            for doc in docs:
                doc_id = doc["doc_id"]
                doc_info = {
                    'kb_id': kb_id,
                    'doc_id': doc_id,
                    'title': f"{doc_id} ({kb_id})"  # Utiliser doc_id comme titre si pas de titre disponible
                }
                all_docs.append(doc_info)
        
        # Si aucun document disponible
        if not all_docs:
            st.info("Aucun document disponible dans les bases sélectionnées.")
            chat_state.selected_docs = []
            StateManager.update_chat_state(chat_state)
            return
            
        # Créer les options pour la sélection
        doc_options = {doc['title']: doc['doc_id'] for doc in all_docs}
        
        # Sélection multiple de documents
        selected_doc_titles = st.multiselect(
            "Filtrer par documents",
            options=list(doc_options.keys()),
            default=[title for title, doc_id in doc_options.items() if doc_id in chat_state.selected_docs],
            format_func=lambda x: x
        )
        
        # Mettre à jour l'état avec les documents sélectionnés
        new_selected_docs = [doc_options[title] for title in selected_doc_titles]
        if new_selected_docs != chat_state.selected_docs:
            chat_state.selected_docs = new_selected_docs
            StateManager.update_chat_state(chat_state)
