"""
Implémentation Streamlit du rendu des chats.
"""
import streamlit as st
from typing import Optional, Iterator, List, Any, ContextManager
from contextlib import contextmanager
from src.ui.interfaces.renderers.chat import IChatRenderer

class StreamlitChatRenderer(IChatRenderer):
    """Implémentation Streamlit du rendu des chats."""
    
    def render_info(self, message: str) -> None:
        """Affiche un message d'information."""
        st.info(message)
    
    def render_success(self, message: str) -> None:
        """Affiche un message de succès."""
        st.success(message)
    
    def render_error(self, message: str) -> None:
        """Affiche un message d'erreur."""
        st.error(message)
    
    def render_markdown(self, content: str) -> None:
        """Affiche du contenu markdown."""
        st.markdown(content)
    
    def render_chat_input(self, placeholder: str) -> Optional[str]:
        """Affiche une zone de saisie de chat."""
        return st.chat_input(placeholder)
    
    @contextmanager
    def chat_message(self, role: str) -> ContextManager[None]:
        """Contexte pour un message de chat."""
        with st.chat_message(role) as msg:
            yield msg
    
    @contextmanager
    def expander(self, label: str, expanded: bool = False) -> ContextManager[None]:
        """Contexte pour un expander."""
        with st.expander(label=label, expanded=expanded) as exp:
            yield exp
    
    def columns(self, n: int) -> List[Any]:
        """Crée des colonnes."""
        return st.columns(n)
    
    def render_code(self, code: str, language: str = "python") -> None:
        """Affiche du code avec coloration syntaxique."""
        st.code(code, language=language)
        
    def render_divider(self) -> None:
        """Affiche une ligne de séparation."""
        st.divider()
        
    @contextmanager
    def container(self) -> ContextManager[None]:
        """Crée un conteneur pour grouper des éléments."""
        with st.container():
            yield
