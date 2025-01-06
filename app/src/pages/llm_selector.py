"""
Composant de sélection de l'API LLM.
"""
import streamlit as st
from dsrag.llm import OpenAIChatAPI, AnthropicChatAPI

class LLMSelector:
    """Composant pour sélectionner l'API LLM à utiliser."""
    
    # Mapping des noms courts vers les noms complets des modèles
    CLAUDE_MODELS = {
        "haiku": "claude-3-haiku-20240307",
        "sonnet": "claude-3-sonnet-20240229",
        "opus": "claude-3-opus-20240229"
    }
    
    OPENAI_MODELS = {
        "3.5-turbo": "gpt-3.5-turbo",
        "4o-mini": "gpt-4o-mini",
        "4o": "gpt-4o"
    }
    
    def __init__(self):
        """Initialise le sélecteur LLM."""
        if 'selected_llm' not in st.session_state:
            st.session_state.selected_llm = 'OpenAI'  # Valeur par défaut
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = '3.5-turbo'  # Valeur par défaut
            
    def get_llm(self):
        """Retourne l'instance LLM appropriée basée sur la sélection."""
        model = st.session_state.selected_model
        if st.session_state.selected_llm == 'OpenAI':
            # Convertir le nom court en nom complet pour OpenAI
            full_model_name = self.OPENAI_MODELS.get(model, model)
            return OpenAIChatAPI(model=full_model_name)
        else:
            # Convertir le nom court en nom complet pour Claude
            full_model_name = self.CLAUDE_MODELS.get(model, model)
            return AnthropicChatAPI(model=full_model_name)
            
    def render(self):
        """Affiche le sélecteur LLM dans la sidebar."""
        selected = st.radio(
            "API LLM",
            options=['OpenAI', 'Anthropic'],
            key='selected_llm',
            horizontal=True
        )
        
        # Sélection du modèle en fonction de l'API choisie
        if st.session_state.selected_llm == 'OpenAI':
            model = st.selectbox(
                "Modèle",
                options=list(self.OPENAI_MODELS.keys()),
                key='selected_model'
            )
        else:
            model = st.selectbox(
                "Modèle",
                options=list(self.CLAUDE_MODELS.keys()),
                key='selected_model'
            )
