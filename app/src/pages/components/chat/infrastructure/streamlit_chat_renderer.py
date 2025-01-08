"""
Implémentation Streamlit du rendu de chat.
"""
import streamlit as st
from contextlib import contextmanager
from typing import List, Optional, Callable, Iterator, Any, BinaryIO
from src.pages.interfaces.ui_renderer import IUIRenderer

class StreamlitChatRenderer(IUIRenderer):
    """Implémentation Streamlit du rendu de chat."""
    
    def render_markdown(self, content: str) -> None:
        """Affiche du contenu markdown."""
        st.markdown(content)
    
    def render_info(self, message: str) -> None:
        """Affiche un message d'information."""
        st.info(message)
    
    def render_success(self, message: str) -> None:
        """Affiche un message de succès."""
        st.success(message)
    
    def render_error(self, message: str) -> None:
        """Affiche un message d'erreur."""
        st.error(message)
    
    def render_select(self,
                     label: str,
                     options: List[str],
                     default: Optional[str] = None,
                     on_change: Optional[Callable] = None) -> str:
        """Rend un sélecteur."""
        index = options.index(default) if default in options else 0
        return st.selectbox(
            label=label,
            options=options,
            index=index,
            on_change=on_change
        )
    
    def render_multiselect(self,
                          label: str,
                          options: List[str],
                          default: Optional[List[str]] = None,
                          on_change: Optional[Callable] = None) -> List[str]:
        """Rend un sélecteur multiple."""
        return st.multiselect(
            label=label,
            options=options,
            default=default or [],
            on_change=on_change
        )
    
    def render_chat_input(self, placeholder: str) -> Optional[str]:
        """Affiche une zone de saisie de chat."""
        return st.chat_input(placeholder)
    
    @contextmanager
    def chat_message(self, role: str):
        """Contexte pour un message de chat."""
        with st.chat_message(role):
            yield
    
    @contextmanager
    def expander(self, label: str, expanded: bool = False):
        """Contexte pour un expander."""
        with st.expander(label, expanded=expanded):
            yield
    
    def render_file_uploader(self,
                           label: str,
                           accepted_types: Optional[List[str]] = None) -> Optional[BinaryIO]:
        """Affiche un sélecteur de fichier."""
        return st.file_uploader(label, type=accepted_types)
    
    def render_button(self, label: str) -> bool:
        """Affiche un bouton."""
        return st.button(label)
    
    def render_text_input(self,
                         label: str,
                         value: str = "",
                         placeholder: str = "") -> str:
        """Affiche une zone de saisie de texte."""
        return st.text_input(
            label=label,
            value=value,
            placeholder=placeholder
        )
    
    def render_text_area(self,
                        label: str,
                        value: str = "",
                        placeholder: str = "") -> str:
        """Affiche une zone de saisie de texte multiligne."""
        return st.text_area(
            label=label,
            value=value,
            placeholder=placeholder
        )
    
    def columns(self, n: int) -> List[Any]:
        """Crée des colonnes."""
        return st.columns(n)
