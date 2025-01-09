"""
Implémentation Streamlit du rendu des bases de connaissances.
"""
import streamlit as st
from typing import List, Optional, Any, ContextManager
from contextlib import contextmanager
from src.ui.interfaces.renderers.kb import IKBRenderer

class StreamlitKBRenderer(IKBRenderer):
    """Implémentation Streamlit du rendu des bases de connaissances."""
    
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
    
    def render_text_input(self,
                         label: str,
                         value: str = "",
                         placeholder: str = "",
                         key: Optional[str] = None,
                         help: Optional[str] = None) -> str:
        """Affiche une zone de saisie de texte."""
        return st.text_input(
            label=label,
            value=value,
            placeholder=placeholder,
            key=key,
            help=help
        )
    
    def render_text_area(self,
                        label: str,
                        value: str = "",
                        placeholder: str = "",
                        key: Optional[str] = None,
                        help: Optional[str] = None) -> str:
        """Affiche une zone de saisie de texte multiligne."""
        return st.text_area(
            label=label,
            value=value,
            placeholder=placeholder,
            key=key,
            help=help
        )
    
    def render_select(self,
                     label: str,
                     options: List[str],
                     default: Optional[str] = None,
                     on_change: Optional[callable] = None) -> str:
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
                          on_change: Optional[callable] = None) -> List[str]:
        """Rend un sélecteur multiple."""
        return st.multiselect(
            label=label,
            options=options,
            default=default or [],
            on_change=on_change
        )
    
    def render_button(self, label: str, key: Optional[str] = None) -> bool:
        """Affiche un bouton."""
        button_key = key or f"button_{label.lower().replace(' ', '_')}"
        return st.button(label, key=button_key)
    
    def render_form_submit_button(self, label: str) -> bool:
        """Affiche un bouton de soumission de formulaire."""
        return st.form_submit_button(label=label)
    
    def render_file_uploader(self,
                           label: str,
                           key: Optional[str] = None,
                           accept_multiple_files: bool = False,
                           help: Optional[str] = None,
                           accepted_types: Optional[List[str]] = None) -> Any:
        """Affiche un uploader de fichiers."""
        return st.file_uploader(
            label=label,
            key=key,
            accept_multiple_files=accept_multiple_files,
            help=help,
            type=accepted_types
        )
    
    @contextmanager
    def expander(self, label: str, expanded: bool = False) -> ContextManager[None]:
        """Contexte pour un expander."""
        with st.expander(label=label, expanded=expanded) as exp:
            yield exp

    @contextmanager
    def form(self, key: str) -> ContextManager[None]:
        """Contexte pour un formulaire."""
        with st.form(key=key) as form:
            yield form

    def columns(self, n: int) -> List[Any]:
        """Crée des colonnes."""
        return st.columns(n)
