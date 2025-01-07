"""
Moteur de recherche pour les bases de connaissances.
"""
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple, Any
from src.core.types import DocumentReference, KnowledgeBase
from dsrag.knowledge_base import KnowledgeBase as DsragKnowledgeBase
from dsrag.database.vector.types import MetadataFilter

from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.config import config
from src.core.state_manager import StateManager

class SearchEngine:
    """Moteur de recherche avec stratégies de fallback."""
    
    def __init__(self, storage_directory: Optional[str] = None):
        """Initialise le moteur de recherche."""
        self.kb_manager = KnowledgeBasesManager(storage_directory=storage_directory)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=getattr(logging, config.logging.level.upper()),
            format=config.logging.format
        )

    def search(self, query: str, kb_ids: Optional[List[str]] = None, doc_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Effectue une recherche dans les bases de connaissances.
        
        Args:
            query: Requête de recherche
            kb_ids: Liste des IDs des bases de connaissances à utiliser
            doc_ids: Liste des IDs des documents à utiliser
            
        Returns:
            Liste des résultats de recherche
        """
        try:
            # Récupérer l'état des bases de connaissances
            kb_state = StateManager.get_kb_state()
            chat_state = StateManager.get_chat_state()
            
            # Si aucune base spécifiée, utiliser toutes les bases disponibles
            if not kb_ids:
                kb_ids = [kb.id for kb in kb_state.knowledge_bases]
            
            results = []
            for kb_id in kb_ids:
                # Obtenir la base de connaissances DSRAG via le manager
                dsrag_kb = self.kb_manager.get_knowledge_base(kb_id)
                if not dsrag_kb:
                    continue
                    
                # Créer le filtre de métadonnées si des documents sont spécifiés
                metadata_filter = self._create_metadata_filter(dsrag_kb, doc_ids) if doc_ids else None
                
                # Effectuer la recherche
                kb_results = dsrag_kb.search(
                    query=query,
                    metadata_filter=metadata_filter,
                    limit=config.search.max_results_per_kb
                )
                
                # Convertir les résultats en références de documents
                for result in kb_results:
                    doc_ref = self._create_document_reference(result, kb_id, "search")
                    if doc_ref:
                        results.append(doc_ref)
            
            # Mettre à jour l'état de la recherche
            chat_state.last_query = query
            chat_state.search_results = results
            StateManager.update_chat_state(chat_state)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche : {str(e)}")
            chat_state.error_message = f"Une erreur est survenue lors de la recherche : {str(e)}"
            StateManager.update_chat_state(chat_state)
            return []

    @staticmethod
    def _create_metadata_filter(kb: DsragKnowledgeBase, doc_ids: List[str]) -> Optional[MetadataFilter]:
        """Crée un filtre de métadonnées pour les documents sélectionnés."""
        if not doc_ids:
            return None
            
        # Filtrer les IDs de documents qui existent dans la base
        valid_doc_ids = [
            doc_id for doc_id in doc_ids
            if doc_id in [doc.get('doc_id') for doc in kb.list_documents()]
        ]
        
        if not valid_doc_ids:
            return None
            
        return {
            "field": "doc_id",
            "operator": "in",
            "value": valid_doc_ids
        }

    @staticmethod
    def _create_document_reference(result: Dict[str, Any], kb_id: str, search_mode: str) -> Optional[Dict[str, Any]]:
        """Crée une référence de document à partir d'un résultat de recherche."""
        try:
            metadata = result.get('metadata', {})
            return {
                "kb_id": kb_id,
                "doc_id": metadata.get('doc_id', ''),
                "title": metadata.get('title', 'Sans titre'),
                "excerpt": result.get('text', ''),
                "score": result.get('score', 0),
                "search_mode": search_mode
            }
        except KeyError:
            return None
