"""
Logique métier pour le chat.
"""
from typing import List, Dict, Any, Optional, Tuple, cast
from uuid import uuid4
from src.ui.interfaces.state_manager import IStateManager
from src.ui.interfaces.chat import (
    IChatSourceManager,
    IChatResponseGenerator,
    IChatSearchManager,
    ChatMessage,
    Source
)
from src.core.state_manager import StateManager

class ChatLogic:
    """Logique métier pour le chat."""
    
    def __init__(self,
                 state_manager: Optional[IStateManager] = None,
                 source_manager: Optional[IChatSourceManager] = None,
                 response_generator: Optional[IChatResponseGenerator] = None,
                 search_manager: Optional[IChatSearchManager] = None):
        """Initialise la logique du chat.
        
        Args:
            state_manager: Gestionnaire d'état
            source_manager: Gestionnaire des sources
            response_generator: Générateur de réponses
            search_manager: Gestionnaire de recherche
        """
        self.state_manager = state_manager or StateManager
        self.source_manager = source_manager
        self.response_generator = response_generator
        self.search_manager = search_manager
    
    def get_messages(self) -> List[ChatMessage]:
        """Récupère les messages du chat.
        
        Returns:
            Liste des messages avec leurs sources
        """
        chat_state = self.state_manager.get_chat_state()
        return [cast(ChatMessage, msg) for msg in chat_state.messages]
    
    def has_selected_kbs(self) -> bool:
        """Vérifie si des bases sont sélectionnées.
        
        Returns:
            True si au moins une base est sélectionnée
        """
        chat_state = self.state_manager.get_chat_state()
        return bool(chat_state.selected_kbs)
        
    def add_user_message(self, message: str) -> None:
        """Ajoute un message utilisateur à l'historique.
        
        Args:
            message: Message de l'utilisateur
        """
        chat_state = self.state_manager.get_chat_state()
        user_message = cast(ChatMessage, {
            "id": str(uuid4()),
            "role": "user",
            "content": message,
            "sources": None
        })
        chat_state.messages.append(user_message)
        self.state_manager.update_chat_state(chat_state)
        
    def generate_response(self, user_input: str) -> Tuple[str, List[Source]]:
        """Génère une réponse à partir d'un message utilisateur.
        
        Args:
            user_input: Message de l'utilisateur
            
        Returns:
            Tuple contenant la réponse et les sources associées
        """
        if not self.search_manager or not self.response_generator or not self.source_manager:
            return "Services non initialisés.", []
            
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
                sources: List[Source] = []
            else:
                # Générer la réponse
                response_content = self.response_generator.generate_response(user_input, results)
                # Formater les sources
                sources = self.source_manager.format_sources(results)
            
            # Préparer la réponse
            response = cast(ChatMessage, {
                "id": str(uuid4()),
                "role": "assistant",
                "content": response_content,
                "sources": sources
            })
            
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
