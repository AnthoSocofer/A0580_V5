"""
Gestionnaire de recherche pour le chat.
"""
from typing import List, Dict, Any
from src.pages.interfaces.chat import IChatSearchManager
from src.core.search_engine import SearchEngine
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.state_manager import StateManager

class ChatSearchManager(IChatSearchManager):
    """Gestionnaire pour la recherche dans les bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise le gestionnaire de recherche.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
        self.search_engine = SearchEngine()
    
    def search_relevant_content(self, 
                              query: str,
                              kb_ids: List[str]) -> List[Dict[str, Any]]:
        """Recherche du contenu pertinent.
        
        Args:
            query: Requête de recherche
            kb_ids: IDs des bases à rechercher
            
        Returns:
            List[Dict[str, Any]]: Résultats de recherche
        """
        # Récupérer les bases de connaissances
        knowledge_bases = []
        for kb_id in kb_ids:
            kb = self.kb_manager.get_knowledge_base(kb_id)
            if kb:
                knowledge_bases.append(kb)
        
        # Effectuer la recherche
        try:
            chat_state = StateManager.get_chat_state()
            results = self.search_engine.search_knowledge_bases(
                query=query,
                knowledge_bases=knowledge_bases,
                selected_kbs=kb_ids,
                selected_docs=chat_state.selected_docs
            )
            
            # Formater les résultats
            formatted_results = []
            for result in results:
                formatted_result = {
                    "kb_id": result.kb_id,
                    "doc_id": result.doc_id,
                    "excerpt": result.text,
                    "score": result.relevance_score,
                    "page_start": result.page_numbers[0],
                    "page_end": result.page_numbers[1],
                    "search_mode": result.search_mode
                }
                formatted_results.append(formatted_result)
                
            return formatted_results
            
        except Exception as e:
            return []
