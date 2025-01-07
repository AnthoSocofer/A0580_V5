"""
Opérations sur les bases de connaissances.
"""
import streamlit as st
from typing import List, Dict, Any
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.types import Document, AutoContextConfig

class KBOperations:
    """Opérations sur les bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise les opérations avec le gestionnaire de bases.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
    
    def _convert_document_dict(self, doc_dict: Dict[str, Any]) -> Document:
        """Convertit un dictionnaire en objet Document.
        
        Args:
            doc_dict: Dictionnaire contenant les données du document
            
        Returns:
            Document converti
        """
        return Document(
            filename=doc_dict["doc_id"],
            title=doc_dict.get("title", ""),
            description=doc_dict.get("description", ""),
            page_count=doc_dict.get("page_count"),
            metadata=doc_dict.get("metadata", {})
        )
    
    def get_knowledge_bases(self) -> List[Dict[str, Any]]:
        """Récupère la liste des bases de connaissances.
        
        Returns:
            Liste des métadonnées des bases de connaissances
        """
        return self.kb_manager.list_knowledge_bases()
    
    def create_knowledge_base(self, kb_id: str, title: str, description: str = "") -> None:
        """Crée une nouvelle base de connaissances.
        
        Args:
            kb_id: Identifiant de la base
            title: Titre de la base
            description: Description de la base
            
        Raises:
            Exception: Si la base existe déjà
        """
        try:
            # Vérifier si la base existe déjà
            existing_kbs = self.get_knowledge_bases()
            if any(kb["kb_id"] == kb_id for kb in existing_kbs):
                raise Exception(f"Une base avec l'ID '{kb_id}' existe déjà!")
                
            # Créer la base
            self.kb_manager.create_knowledge_base(
                kb_id=kb_id,
                title=title,
                description=description
            )
            
            # Mettre à jour l'état avec les métadonnées
            kb_state = StateManager.get_kb_state()
            kb_state.knowledge_bases_metadata = self.kb_manager.list_knowledge_bases()
            StateManager.update_kb_state(kb_state)
            
            st.success(f"Base '{title}' créée avec succès!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur lors de la création: {str(e)}")
    
    def delete_knowledge_base(self, kb_id: str) -> None:
        """Supprime une base de connaissances.
        
        Args:
            kb_id: Identifiant de la base à supprimer
        """
        try:
            # Supprimer la base
            self.kb_manager.delete_knowledge_base(kb_id)
            
            # Mettre à jour l'état
            kb_state = StateManager.get_kb_state()
            kb_state.knowledge_bases_metadata = self.kb_manager.list_knowledge_bases()
            if kb_state.current_kb_id == kb_id:
                kb_state.current_kb_metadata = None
                kb_state.current_kb_id = None
            StateManager.update_kb_state(kb_state)
            
            st.success(f"Base '{kb_id}' supprimée avec succès!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {str(e)}")
    
    def add_document(self, kb_id: str, doc_id: str, file_path: str, auto_context_config: AutoContextConfig) -> Document:
        """Ajoute un document à une base de connaissances.
        
        Args:
            kb_id: Identifiant de la base
            doc_id: Identifiant du document
            file_path: Chemin vers le fichier
            auto_context_config: Configuration pour le contexte automatique
            
        Returns:
            Le document ajouté
        """
        doc_dict = self.kb_manager.add_document(
            kb_id=kb_id,
            doc_id=doc_id,
            file_path=file_path,
            auto_context_config=auto_context_config
        )
        return self._convert_document_dict(doc_dict)
    
    def delete_document(self, kb_id: str, doc_id: str) -> None:
        """Supprime un document d'une base de connaissances.
        
        Args:
            kb_id: Identifiant de la base
            doc_id: Identifiant du document
        """
        self.kb_manager.delete_document(kb_id, doc_id)
