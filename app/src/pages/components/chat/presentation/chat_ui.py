"""
Interface utilisateur pour le chat.
"""
from typing import Optional, Dict, Any
from src.pages.interfaces.ui_renderer import IUIRenderer
from src.pages.components.chat.domain.chat_logic import ChatLogic

class ChatUI:
    """Interface utilisateur pour le chat."""
    
    def __init__(self,
                 chat_logic: ChatLogic,
                 ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur."""
        self.chat_logic = chat_logic
        self.ui_renderer = ui_renderer
    
    def render(self) -> None:
        """Affiche l'interface de chat."""
        self.ui_renderer.render_markdown("## 💬 Discussion")
        
        if not self.chat_logic.has_selected_kbs():
            self.ui_renderer.render_info(
                "Sélectionnez au moins une base de connaissances dans la barre latérale pour commencer."
            )
            return
        
        # Affichage des messages
        for message in self.chat_logic.get_messages():
            self._render_message(message)
        
        # Zone de saisie
        user_input = self.ui_renderer.render_chat_input("Votre message")
        if user_input:
            self._handle_user_input(user_input)
    
    def _render_message(self, message: Dict[str, Any]) -> None:
        """Affiche un message."""
        with self.ui_renderer.chat_message(message["role"]):
            self.ui_renderer.render_markdown(message["content"])
            
            # Affichage des sources
            if message.get("sources"):
                with self.ui_renderer.expander("📚 Sources", expanded=False):
                    for source in message["sources"]:
                        self.ui_renderer.render_markdown(f"**Document**: {source['title']}")
                        if source.get("score"):
                            self.ui_renderer.render_markdown(
                                f"*Score de pertinence*: {source['score']:.2f}"
                            )
                        if source.get("pages"):
                            self.ui_renderer.render_markdown(f"*{source['pages']}*")
    
    def _handle_user_input(self, user_input: str) -> None:
        """Gère l'entrée utilisateur."""
        # Ajout du message utilisateur
        self.chat_logic.add_user_message(user_input)
        
        # Génération de la réponse
        response, sources = self.chat_logic.generate_response(user_input)
        
        # Ajout de la réponse
        self.chat_logic.add_assistant_message(response, sources)
