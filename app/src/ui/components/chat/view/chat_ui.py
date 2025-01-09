"""
Interface utilisateur pour le chat.
"""
from typing import Dict, Any, cast, List
from src.ui.interfaces.renderers.chat import IChatRenderer
from src.ui.interfaces.chat import ChatMessage, Source
from src.ui.components.chat.business.chat_logic import ChatLogic

class ChatUI:
    """Interface utilisateur pour le chat."""
    
    def __init__(self,
                 chat_logic: ChatLogic,
                 ui_renderer: IChatRenderer):
        """Initialise l'interface utilisateur.
        
        Args:
            chat_logic: Logique métier du chat
            ui_renderer: Renderer pour l'interface utilisateur
        """
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
    
    def _render_message(self, message: ChatMessage) -> None:
        """Affiche un message.
        
        Args:
            message: Message à afficher avec ses métadonnées
        """
        with self.ui_renderer.chat_message(message["role"]):
            self.ui_renderer.render_markdown(message["content"])
            
            # Affichage des sources
            if message.get("sources"):
                self._render_sources(cast(List[Source], message["sources"]))
                self._render_source_summary(cast(List[Source], message["sources"]))
    
    def _get_relevance_color(self, score: float) -> str:
        """Détermine la couleur d'affichage en fonction du score.
        
        Args:
            score: Score de pertinence
            
        Returns:
            Emoji de couleur correspondant au score
        """
        if score >= 0.8:
            return "🟢"  # Très pertinent
        elif score >= 0.6:
            return "🟡"  # Moyennement pertinent
        else:
            return "🔴"  # Peu pertinent
    
    def _render_sources(self, sources: List[Source]) -> None:
        """Affiche les sources dans un expander.
        
        Args:
            sources: Liste des sources à afficher
        """
        with self.ui_renderer.expander("📚 Voir toutes les sources en détail", expanded=False):
            self.ui_renderer.render_markdown("### Documents pertinents trouvés")
            
            for idx, source in enumerate(sources, 1):
                with self.ui_renderer.container():
                    # En-tête avec score et métadonnées
                    header_cols = self.ui_renderer.columns(3)
                    
                    with header_cols[0]:
                        color = self._get_relevance_color(source["score"])
                        self.ui_renderer.render_markdown(f"**Source {idx}**  \n{color}")
                        self.ui_renderer.render_markdown(f"Score: **{source['score']:.2f}**")
                        
                    with header_cols[1]:
                        self.ui_renderer.render_markdown(f"""
                        **Document**: {source['title']}  
                        **Base**: {source['kb_id']}
                        """)
                        
                    with header_cols[2]:
                        if source.get("page_numbers"):
                            start, end = source["page_numbers"][:2]
                            self.ui_renderer.render_markdown(f"**Pages**: {start}-{end}")
                    
                    # Extrait du document
                    if source.get("excerpt"):
                        self.ui_renderer.render_markdown("**Extrait pertinent:**")
                        self.ui_renderer.render_code(source["excerpt"], language="text")
                    
                    # Contenu complet si disponible
                    if source.get("content") and source["content"] != source.get("excerpt"):
                        self.ui_renderer.render_markdown("**Contenu complet:**")
                        self.ui_renderer.render_code(source["content"], language="text")
                    
                    self.ui_renderer.render_divider()
    
    def _render_source_summary(self, sources: List[Source]) -> None:
        """Affiche un résumé des sources principales.
        
        Args:
            sources: Liste des sources à résumer
        """
        # Ne montrer que les sources les plus pertinentes
        relevant_sources = [s for s in sources if s["score"] >= 0.5][:3]
        
        if relevant_sources:
            self.ui_renderer.render_markdown("---")
            self.ui_renderer.render_markdown("**Sources principales utilisées:**")
            
            for idx, source in enumerate(relevant_sources, 1):
                if source.get("page_numbers"):
                    start, end = source["page_numbers"][:2]
                    pages = f"p. {start}-{end}"
                else:
                    pages = ""
                    
                self.ui_renderer.render_markdown(
                    f"- 📄 **Source {idx}** ({source['score']:.2f}): "
                    f"{source['title']} ({pages})"
                )
    
    def _handle_user_input(self, user_input: str) -> None:
        """Gère l'entrée utilisateur.
        
        Args:
            user_input: Message saisi par l'utilisateur
        """
        # Ajout et affichage du message utilisateur
        self.chat_logic.add_user_message(user_input)
        with self.ui_renderer.chat_message("user"):
            self.ui_renderer.render_markdown(user_input)
        
        # Génération de la réponse
        response, sources = self.chat_logic.generate_response(user_input)
        
        # Affichage de la réponse
        with self.ui_renderer.chat_message("assistant"):
            self.ui_renderer.render_markdown(response)
            if sources:
                self._render_sources(sources)
                self._render_source_summary(sources)
