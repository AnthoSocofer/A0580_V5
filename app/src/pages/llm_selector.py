"""
Composant de sélection de l'API LLM.
"""
import streamlit as st
from dsrag.llm import OpenAIChatAPI, AnthropicChatAPI

class LLMSelector:
    """Composant pour sélectionner l'API LLM à utiliser."""
    
    def __init__(self):
        """Initialise le sélecteur LLM."""
        if 'selected_llm' not in st.session_state:
            st.session_state.selected_llm = 'OpenAI'  # Valeur par défaut
            
    def get_llm(self):
        """Retourne l'instance LLM appropriée basée sur la sélection."""
        if st.session_state.selected_llm == 'OpenAI':
            return OpenAIChatAPI()
        else:
            return AnthropicChatAPI()
            
    def render(self):
        """Affiche le sélecteur LLM dans la sidebar."""
        st.markdown("### Sélection du modèle")
        selected = st.radio(
            "API LLM",
            options=['OpenAI', 'Anthropic'],
            key='selected_llm',
            horizontal=True
        )
