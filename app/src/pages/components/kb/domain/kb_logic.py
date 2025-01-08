"""
Logique métier pour la gestion des bases de connaissances.
"""
from typing import List, Dict, Any, Optional
from src.pages.interfaces.state_manager import IStateManager
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class KBLogic:
    """Logique métier pour la gestion des bases de connaissances."""
    
    def __init__(self,
                 kb_manager: KnowledgeBasesManager,
                 state_manager: Optional[IStateManager] = None):
        """Initialise la logique.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
            state_manager: Gestionnaire d'état
        """
        self.kb_manager = kb_manager
        self.state_manager = state_manager or StateManager
    
    def get_knowledge_bases(self) -> List[Dict[str, Any]]:
        """Récupère la liste des bases de connaissances."""
        return self.kb_manager.get_knowledge_bases()
    
    def create_knowledge_base(self, title: str, description: str) -> str:
        """Crée une nouvelle base de connaissances.
        
        Args:
            title: Titre de la base
            description: Description de la base
            
        Returns:
            str: ID de la base créée
        """
        return self.kb_manager.create_knowledge_base(title, description)
    
    def delete_knowledge_base(self, kb_id: str) -> None:
        """Supprime une base de connaissances.
        
        Args:
            kb_id: ID de la base à supprimer
        """
        self.kb_manager.delete_knowledge_base(kb_id)
    
    def upload_document(self, kb_id: str, file_content: bytes, filename: str) -> str:
        """Upload un document dans une base.
        
        Args:
            kb_id: ID de la base
            file_content: Contenu du fichier
            filename: Nom du fichier
            
        Returns:
            str: ID du document créé
        """
        return self.kb_manager.upload_document(kb_id, file_content, filename)
    
    def delete_document(self, kb_id: str, doc_id: str) -> None:
        """Supprime un document d'une base.
        
        Args:
            kb_id: ID de la base
            doc_id: ID du document
        """
        self.kb_manager.delete_document(kb_id, doc_id)
    
    def get_active_kb(self) -> Optional[str]:
        """Récupère l'ID de la base active."""
        return self.state_manager.get_kb_state().active_kb
    
    def set_active_kb(self, kb_id: str) -> None:
        """Définit la base active.
        
        Args:
            kb_id: ID de la base à activer
        """
        kb_state = self.state_manager.get_kb_state()
        kb_state.active_kb = kb_id
        self.state_manager.update_kb_state(kb_state)
