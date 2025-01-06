"""
Composant de sélection de l'API LLM.
"""
import streamlit as st
from dsrag.llm import OpenAIChatAPI, AnthropicChatAPI
from src.core.state_manager import StateManager

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
        StateManager.initialize_states()
            
    def get_llm(self):
        """Retourne l'instance LLM appropriée basée sur la sélection."""
        llm_state = StateManager.get_llm_state()
        model = llm_state.selected_model
        if llm_state.selected_llm == 'OpenAI':
            # Convertir le nom court en nom complet pour OpenAI
            full_model_name = self.OPENAI_MODELS.get(model, model)
            return OpenAIChatAPI(model=full_model_name)
        else:
            # Convertir le nom court en nom complet pour Claude
            full_model_name = self.CLAUDE_MODELS.get(model, model)
            return AnthropicChatAPI(model=full_model_name)
            
    def render(self):
        """Affiche le sélecteur LLM dans la sidebar."""
        llm_state = StateManager.get_llm_state()
        
        # Sélection de l'API
        selected_llm = st.radio(
            "API LLM",
            options=['OpenAI', 'Anthropic'],
            index=0 if llm_state.selected_llm == 'OpenAI' else 1,
            horizontal=True,
            key='selected_llm'
        )
        
        # Mise à jour de l'état si changé
        if selected_llm != llm_state.selected_llm:
            llm_state.selected_llm = selected_llm
            # Réinitialiser le modèle au défaut pour la nouvelle API
            llm_state.selected_model = "3.5-turbo" if selected_llm == "OpenAI" else "haiku"
            StateManager.update_llm_state(llm_state)
        
        # Sélection du modèle en fonction de l'API
        models = self.OPENAI_MODELS.keys() if selected_llm == 'OpenAI' else self.CLAUDE_MODELS.keys()
        selected_model = st.selectbox(
            "Modèle",
            options=list(models),
            key='selected_model'
        )
        
        # Mise à jour de l'état si changé
        if selected_model != llm_state.selected_model:
            llm_state.selected_model = selected_model
            StateManager.update_llm_state(llm_state)
