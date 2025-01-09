"""
Logique métier pour la création d'une base de connaissances.
"""
from typing import Optional, Dict, Any
from src.ui.interfaces.state_manager import IStateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class KBCreator:
    """Logique métier pour la création d'une base de connaissances."""
    
    def __init__(self,
                 state_manager: IStateManager,
                 kb_manager: KnowledgeBasesManager):
        """Initialise le créateur.
        
        Args:
            state_manager: Gestionnaire d'état
            kb_manager: Gestionnaire des bases de connaissances
        """
        self.state_manager = state_manager
        self.kb_manager = kb_manager
    
    def create_knowledge_base(self,
                            kb_id: str,
                            title: str,
                            description: Optional[str] = None) -> None:
        """Crée une nouvelle base de connaissances.
        
        Args:
            kb_id: Identifiant unique de la base
            title: Titre de la base
            description: Description optionnelle de la base
        """
        # Vérifie si la base existe déjà
        existing_kbs = self.kb_manager.get_knowledge_bases()
        if kb_id in existing_kbs:
            raise ValueError(f"Une base avec l'ID '{kb_id}' existe déjà!")
            
        # Crée la base
        self.kb_manager.create_knowledge_base(kb_id, title, description)

    def get_knowledge_bases(self) -> Dict[str, Any]:
        """Récupère la liste des bases de connaissances.
        
        Returns:
            Dictionnaire des bases de connaissances indexé par ID
        """
        return self.kb_manager.get_knowledge_bases()
