"""
Logique métier pour le filtrage des documents.
"""
from typing import List, Dict, Any, Optional
from src.pages.interfaces.state_manager import IStateManager
from src.pages.interfaces.filter import IFilterLogic
from src.pages.interfaces.kb_infrastructure import IKnowledgeBaseStore
from src.core.state_manager import StateManager

class DocumentFilterLogic:
    """Logique de filtrage des documents."""

    def __init__(self, 
                 state_manager: IStateManager,
                 kb_store: IKnowledgeBaseStore):
        """Initialise la logique de filtrage des documents."""
        self.state_manager = state_manager
        self.kb_store = kb_store
        self._initialize_state()

    def _initialize_state(self):
        """Initialise l'état du filtre si nécessaire."""
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
        if not hasattr(chat_state, 'selected_document_types'):
            chat_state.selected_document_types = []
        self.state_manager.update_chat_state(chat_state)

    def handle_kb_selection(self, selected_kbs: List[str]):
        """Gère la sélection des bases de connaissances.
        
        Args:
            selected_kbs: Liste des IDs des bases sélectionnées
        """
        chat_state = self.state_manager.get_chat_state()
        chat_state.selected_kbs = selected_kbs
        if not selected_kbs:  # Si aucune base sélectionnée, vider aussi la sélection des documents
            chat_state.selected_docs = []
        self.state_manager.update_chat_state(chat_state)

    def handle_doc_selection(self, selected_docs: List[str]):
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
                
        # Appliquer le filtre sur les types de documents
        return self.apply_document_type_filter(all_docs)

    def get_selected_documents(self) -> List[str]:
        """Récupère les documents sélectionnés."""
        chat_state = self.state_manager.get_chat_state()
        return chat_state.selected_docs

    def get_available_document_types(self) -> List[str]:
        """Récupère tous les types de documents disponibles dans la base de connaissances."""
        knowledge_bases = self.kb_store.list_knowledge_bases()
        document_types = set()
        
        # Récupérer les types de documents depuis les documents de chaque base
        for kb in knowledge_bases:
            for doc in kb.get('documents', []):
                doc_type = doc.get('type')
                if doc_type:
                    document_types.add(doc_type)
        
        return sorted(list(document_types))

    def get_selected_document_types(self) -> List[str]:
        """Récupère les types de documents actuellement sélectionnés."""
        chat_state = self.state_manager.get_chat_state()
        return chat_state.selected_document_types

    def set_selected_document_types(self, types: List[str]) -> None:
        """Définit les types de documents sélectionnés."""
        chat_state = self.state_manager.get_chat_state()
        chat_state.selected_document_types = types
        self.state_manager.update_chat_state(chat_state)

    def apply_document_type_filter(self, documents: List[dict]) -> List[dict]:
        """Applique le filtre sur les types de documents."""
        selected_types = self.get_selected_document_types()
        if not selected_types:  # Si aucun type n'est sélectionné, retourne tous les documents
            return documents
        return [doc for doc in documents if doc.get('type') in selected_types]
