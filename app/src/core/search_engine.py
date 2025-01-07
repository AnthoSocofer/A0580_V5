"""
Moteur de recherche pour les bases de connaissances.
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple, Any
from src.core.types import DocumentReference
from dsrag.knowledge_base import KnowledgeBase
from dsrag.database.vector.types import MetadataFilter

from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.config import config

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

    @staticmethod
    def _create_metadata_filter(kb: KnowledgeBase, selected_docs: List[str]) -> Optional[MetadataFilter]:
        """Crée un filtre de métadonnées pour les documents sélectionnés."""
        if not selected_docs:
            return None
            
        # Utiliser l'API du chunk_db pour obtenir les IDs des documents
        kb_doc_ids = kb.chunk_db.get_all_doc_ids()
        selected_docs_in_kb = [
            doc_id for doc_id in selected_docs
            if doc_id in kb_doc_ids
        ]
        
        if not selected_docs_in_kb:
            return None
            
        return {
            "field": "doc_id",
            "operator": "in",
            "value": selected_docs_in_kb
        }

    @staticmethod
    def _create_document_reference(
        result: Dict,
        kb: KnowledgeBase,
        search_mode: str,
        is_query_result: bool = True
    ) -> DocumentReference:
        """Crée une référence de document à partir d'un résultat de recherche."""
        if is_query_result:
            return DocumentReference(
                doc_id=result["doc_id"],
                kb_id=kb.kb_id if hasattr(kb, 'kb_id') else "",
                text=result["content"],
                relevance_score=result.get("score", 0),
                page_numbers=(
                    result.get("segment_page_start", 0),
                    result.get("segment_page_end", 0)
                ),
                search_mode=search_mode
            )
        else:
            metadata = result.get("metadata", {})
            doc_id = metadata.get("doc_id", "")
            chunk_index = metadata.get("chunk_index", 0)
            
            page_start, page_end = kb.get_segment_page_numbers(
                doc_id=doc_id,
                chunk_start=chunk_index,
                chunk_end=chunk_index + 1
            )
            
            return DocumentReference(
                doc_id=doc_id,
                kb_id=kb.kb_id if hasattr(kb, 'kb_id') else "",
                text=metadata.get("chunk_text", ""),
                relevance_score=result.get("similarity", 0),
                page_numbers=(page_start, page_end),
                search_mode=search_mode
            )

    def _query_knowledge_base(
        self,
        kb: KnowledgeBase,
        query: str,
        metadata_filter: Optional[MetadataFilter],
        mode: str
    ) -> List[DocumentReference]:
        """Effectue une recherche via query() avec un mode spécifique."""
        try:
            results = kb.query(
                search_queries=[query],
                rse_params=mode,
                return_mode="text",
                metadata_filter=metadata_filter
            )
            
            return [
                self._create_document_reference(result, kb, mode)
                for result in results
            ]
            
        except Exception as e:
            self.logger.warning(f"Erreur lors de la recherche en mode {mode}: {str(e)}")
            return []

    def _search_knowledge_base(
        self,
        kb: KnowledgeBase,
        query: str,
        metadata_filter: Optional[MetadataFilter]
    ) -> List[DocumentReference]:
        """Effectue une recherche directe via search()."""
        try:
            results = kb.search(
                query=query,
                metadata_filter=metadata_filter
            )
            
            return [
                self._create_document_reference(result, kb, "search", is_query_result=False)
                for result in results
            ]
            
        except Exception as e:
            self.logger.warning(f"Erreur lors de la recherche directe: {str(e)}")
            return []

    def search_knowledge_bases(
        self,
        query: str,
        knowledge_bases: List[KnowledgeBase],
        selected_kbs: Optional[List[str]] = None,
        selected_docs: Optional[List[str]] = None
    ) -> List[DocumentReference]:
        """Recherche dans les bases de connaissances avec stratégie de fallback.
        
        Args:
            query: Requête de recherche
            knowledge_bases: Liste des bases de connaissances
            selected_kbs: Liste des IDs des bases sélectionnées (optionnel)
            selected_docs: Liste des IDs des documents sélectionnés (optionnel)
            
        Returns:
            Liste des références de documents trouvés
        """
        all_results = []
        
        # Filtrer les bases si une sélection est fournie
        if selected_kbs:
            knowledge_bases = [
                kb for kb in knowledge_bases
                if kb.kb_id in selected_kbs
            ]
        
        for kb in knowledge_bases:
            try:
                # Créer le filtre de documents si nécessaire
                metadata_filter = self._create_metadata_filter(kb, selected_docs or [])
                
                # Essayer d'abord la recherche avec query()
                results = []
                for mode in ["balanced", "fast"]:
                    if not results:
                        results = self._query_knowledge_base(kb, query, metadata_filter, mode)
                
                # Si aucun résultat, essayer la recherche directe
                if not results:
                    results = self._search_knowledge_base(kb, query, metadata_filter)
                
                all_results.extend(results)
                
            except Exception as e:
                self.logger.error(f"Erreur lors de la recherche dans {kb.kb_id}: {str(e)}")
                continue
        
        # Trier les résultats par score de pertinence
        all_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return all_results