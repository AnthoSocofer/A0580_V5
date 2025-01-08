"""
Implémentation Streamlit du rendu UI.
"""
import streamlit as st
from typing import List, Optional, Callable
from src.ui.interfaces.ui_renderer import IUIRenderer

class StreamlitUIRenderer(IUIRenderer):
    """Implémentation Streamlit du rendu UI."""
    
    def render_select(self,
                     label: str,
                     options: List[str],
                     default: Optional[str] = None,
                     on_change: Optional[Callable] = None) -> str:
        """Rend un sélecteur avec Streamlit."""
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
        """Rend un sélecteur multiple avec Streamlit."""
        return st.multiselect(
            label=label,
            options=options,
            default=default or [],
            on_change=on_change
        )
    
    def render_info(self, message: str) -> None:
        """Affiche un message d'information avec Streamlit."""
        st.info(message)
