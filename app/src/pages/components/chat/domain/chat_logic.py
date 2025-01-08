"""
Logique métier pour le chat.
"""
from typing import List, Dict, Any, Optional
from src.pages.interfaces.state_manager import IStateManager
from src.pages.interfaces.chat import (
    IChatSourceManager,
    IChatResponseGenerator,
    IChatSearchManager
)
from src.core.state_manager import StateManager

class ChatLogic:
    """Logique métier pour le chat."""
    
    def __init__(self,
                 state_manager: Optional[IStateManager] = None,
                 source_manager: Optional[IChatSourceManager] = None,
                 response_generator: Optional[IChatResponseGenerator] = None,
                 search_manager: Optional[IChatSearchManager] = None):
        """Initialise la logique du chat."""
        self.state_manager = state_manager or StateManager
        self.source_manager = source_manager
        self.response_generator = response_generator
        self.search_manager = search_manager
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Récupère les messages du chat."""
        chat_state = self.state_manager.get_chat_state()
        return chat_state.messages
    
    def check_kb_availability(self) -> bool:
        """Vérifie la disponibilité des bases de connaissances."""
        kb_state = self.state_manager.get_kb_state()
        chat_state = self.state_manager.get_chat_state()
        
        return bool(kb_state.knowledge_bases and chat_state.selected_kbs)
    
    def process_user_message(self, prompt: str) -> Dict[str, Any]:
        """Traite un message utilisateur.
        
        Args:
            prompt: Message de l'utilisateur
            
        Returns:
            Dict[str, Any]: Réponse formatée avec les sources
        """
        chat_state = self.state_manager.get_chat_state()
        
        # Ajouter le message utilisateur
        chat_state.messages.append({
            "role": "user",
            "content": prompt
        })
        self.state_manager.update_chat_state(chat_state)
        
        # Effectuer la recherche
        chat_state.is_processing = True
        self.state_manager.update_chat_state(chat_state)
        
        try:
            # Rechercher les sources
            results = self.search_manager.perform_search(prompt)
            
            if not results:
                response_content = "Je n'ai trouvé aucun document pertinent."
            else:
                # Générer une réponse basée sur les sources
                response_content = self.response_generator.generate_response(prompt, results)
            
            # Formater les sources
            sources = self.source_manager.format_sources(results)
            
            # Préparer la réponse
            response = {
                "role": "assistant",
                "content": response_content,
                "sources": sources
            }
            
            # Mettre à jour l'état
            chat_state.messages.append(response)
            chat_state.is_processing = False
            chat_state.last_query = prompt
            chat_state.search_results = results
            self.state_manager.update_chat_state(chat_state)
            
            return response
            
        except Exception as e:
            error_response = {
                "role": "assistant",
                "content": f"Une erreur est survenue : {str(e)}",
                "sources": []
            }
            chat_state.is_processing = False
            self.state_manager.update_chat_state(chat_state)
            return error_response
    
    def is_processing(self) -> bool:
        """Vérifie si un message est en cours de traitement."""
        chat_state = self.state_manager.get_chat_state()
        return chat_state.is_processing
