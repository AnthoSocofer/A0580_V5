"""
Logique métier pour le chat.
"""
from typing import List, Dict, Any, Optional, Tuple
from src.ui.interfaces.state_manager import IStateManager
from src.ui.interfaces.chat import (
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
    
    def has_selected_kbs(self) -> bool:
        """Vérifie si des bases sont sélectionnées."""
        chat_state = self.state_manager.get_chat_state()
        return bool(chat_state.selected_kbs)
        
    def add_user_message(self, message: str) -> None:
        """Ajoute un message utilisateur à l'historique.
        
        Args:
            message: Message de l'utilisateur
        """
        chat_state = self.state_manager.get_chat_state()
        chat_state.messages.append({
            "role": "user",
            "content": message
        })
        self.state_manager.update_chat_state(chat_state)
        
    def generate_response(self, user_input: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Génère une réponse à partir d'un message utilisateur.
        
        Args:
            user_input: Message de l'utilisateur
            
        Returns:
            Tuple[str, List[Dict[str, Any]]]: Tuple contenant la réponse et les sources
        """
        chat_state = self.state_manager.get_chat_state()
        
        # Marquer comme en cours de traitement
        chat_state.is_processing = True
        self.state_manager.update_chat_state(chat_state)
        
        try:
            # Effectuer la recherche
            results = self.search_manager.search_relevant_content(
                query=user_input,
                kb_ids=chat_state.selected_kbs
            )
            
            if not results:
                response_content = "Je n'ai trouvé aucun document pertinent."
                sources = []
            else:
                # Générer la réponse
                response_content = self.response_generator.generate_response(user_input, results)
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
            chat_state.last_query = user_input
            chat_state.search_results = results
            self.state_manager.update_chat_state(chat_state)
            
            return response_content, sources
            
        except Exception as e:
            error_message = f"Une erreur est survenue : {str(e)}"
            chat_state.is_processing = False
            self.state_manager.update_chat_state(chat_state)
            return error_message, []
