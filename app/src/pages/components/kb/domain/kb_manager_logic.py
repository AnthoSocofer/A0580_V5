"""
Logique métier pour la gestion des bases de connaissances.
"""
from typing import List, Dict, Any, Optional
from src.pages.interfaces.state_manager import IStateManager
from src.pages.interfaces.kb_infrastructure import (
    IKnowledgeBaseProcessor,
    IKnowledgeBaseStore,
    IKnowledgeBaseValidator
)
from src.core.state_manager import StateManager
from src.core.types import KnowledgeBase

class KBManagerLogic:
    """Logique métier pour la gestion des bases de connaissances."""
    
    def __init__(self,
                 state_manager: Optional[IStateManager] = None,
                 kb_processor: Optional[IKnowledgeBaseProcessor] = None,
                 kb_store: Optional[IKnowledgeBaseStore] = None,
                 kb_validator: Optional[IKnowledgeBaseValidator] = None):
        """Initialise la logique de gestion des bases de connaissances."""
        self.state_manager = state_manager or StateManager
        self.kb_processor = kb_processor
        self.kb_store = kb_store
        self.kb_validator = kb_validator
    
    def create_knowledge_base(self, title: str, description: str) -> Optional[str]:
        """Crée une nouvelle base de connaissances."""
        if not all([self.kb_processor, self.kb_store, self.kb_validator]):
            return None
            
        # Validation des données
        if not self.kb_validator.validate_title(title) or \
           not self.kb_validator.validate_description(description):
            return None
        
        # Création de la base
        kb = self.kb_processor.create_knowledge_base(title, description)
        
        # Validation de la base
        if not self.kb_validator.validate_knowledge_base(kb):
            return None
        
        # Sauvegarde de la base
        kb_id = self.kb_store.save_knowledge_base(kb)
        
        # Mise à jour de l'état
        self._update_kb_state()
        
        return kb_id
    
    def list_knowledge_bases(self) -> List[KnowledgeBase]:
        """Liste toutes les bases de connaissances."""
        if not self.kb_store:
            return []
            
        raw_kbs = self.kb_store.list_knowledge_bases()
        
        # Conversion des bases de connaissances
        kbs = []
        for raw_kb in raw_kbs:
            kb = KnowledgeBase(
                id=raw_kb.get('id', ''),
                title=raw_kb.get('title', ''),
                description=raw_kb.get('description', '')
            )
            kbs.append(kb)
            
        return kbs
    
    def delete_knowledge_base(self, kb_id: str) -> bool:
        """Supprime une base de connaissances."""
        if not self.kb_store:
            return False
            
        success = self.kb_store.delete_knowledge_base(kb_id)
        if success:
            self._update_kb_state()
            
        return success
    
    def load_knowledge_bases(self) -> None:
        """Charge les bases de connaissances et met à jour l'état."""
        if not self.kb_store:
            return
            
        # Charger les bases et mettre à jour l'état
        self._update_kb_state()

    def _update_kb_state(self) -> None:
        """Met à jour l'état des bases de connaissances."""
        kb_state = self.state_manager.get_kb_state()
        kb_state.knowledge_bases = self.list_knowledge_bases()
        self.state_manager.update_kb_state(kb_state)
