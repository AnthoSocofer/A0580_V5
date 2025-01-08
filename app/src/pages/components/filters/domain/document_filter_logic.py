"""
Logique métier pour le filtre des documents.
"""
from typing import List, Optional, Dict, Any
from src.pages.interfaces.state_manager import IStateManager
from src.pages.interfaces.kb_infrastructure import IKnowledgeBaseStore
from src.core.state_manager import StateManager

class DocumentFilterLogic:
    """Logique métier pour le filtre des documents."""
    
    def __init__(self,
                 state_manager: Optional[IStateManager] = None,
                 kb_store: Optional[IKnowledgeBaseStore] = None):
        """Initialise la logique de filtrage."""
        self.state_manager = state_manager or StateManager
        self.kb_store = kb_store
        self._initialize_state()
    
    def _initialize_state(self) -> None:
        """Initialise l'état du filtre."""
        chat_state = self.state_manager.get_chat_state()
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
        self.state_manager.update_chat_state(chat_state)
    
    def handle_kb_selection(self, selected_kbs: List[str]) -> None:
        """Gère la sélection des bases de connaissances.
        
        Args:
            selected_kbs: Liste des IDs des bases sélectionnées
        """
        chat_state = self.state_manager.get_chat_state()
        chat_state.selected_kbs = selected_kbs
        if not selected_kbs:  # Si aucune base sélectionnée, vider aussi la sélection des documents
            chat_state.selected_docs = []
        self.state_manager.update_chat_state(chat_state)
    
    def handle_doc_selection(self, selected_docs: List[str]) -> None:
        """Gère la sélection des documents.
        
        Args:
            selected_docs: Liste des IDs des documents sélectionnés
        """
        chat_state = self.state_manager.get_chat_state()
        chat_state.selected_docs = selected_docs
        self.state_manager.update_chat_state(chat_state)
    
    def get_available_documents(self) -> List[Dict[str, Any]]:
        """Récupère la liste des documents disponibles."""
        chat_state = self.state_manager.get_chat_state()
        
        # Initialiser ou mettre à jour le cache des documents
        if not chat_state.cached_documents:
            chat_state.cached_documents = {}
            for kb_id in chat_state.selected_kbs:
                if kb_id not in chat_state.cached_documents:
                    try:
                        kb = self.kb_store.get_knowledge_base(kb_id)
                        if kb:
                            # Obtenir les IDs des documents depuis la base
                            doc_ids = kb.chunk_db.get_all_doc_ids()
                            # Créer les objets document
                            docs = [{"doc_id": doc_id} for doc_id in doc_ids]
                            chat_state.cached_documents[kb_id] = docs
                    except Exception as e:
                        raise RuntimeError(f"Erreur lors de la récupération des documents de {kb_id}: {str(e)}")
            self.state_manager.update_chat_state(chat_state)
        
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
                
        return all_docs
    
    def get_selected_documents(self) -> List[str]:
        """Récupère les documents sélectionnés."""
        chat_state = self.state_manager.get_chat_state()
        return chat_state.selected_docs
