"""
Composant de sélection de l'API LLM.
"""
import streamlit as st
from dsrag.llm import OpenAIChatAPI, AnthropicChatAPI
from src.core.state_manager import StateManager, LLMState

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
        pass
            
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
            
    def on_change(self):
        """Callback when either LLM or model selection changes."""
        llm_state = StateManager.get_llm_state()
        current_llm = st.session_state.selected_llm
        current_model = st.session_state.selected_model
        
        # Seulement mettre à jour si les valeurs ont changé
        if (current_llm != llm_state.selected_llm or 
            current_model != llm_state.selected_model):
            # Si le LLM a changé, réinitialiser le modèle
            if current_llm != llm_state.selected_llm:
                current_model = "3.5-turbo" if current_llm == "OpenAI" else "haiku"
                st.session_state.selected_model = current_model
            
            # Mettre à jour l'état global via StateManager
            new_state = LLMState(
                selected_llm=current_llm,
                selected_model=current_model
            )
            StateManager.update_llm_state(new_state)
            
    def render(self):
        """Affiche le sélecteur LLM dans la sidebar."""
        # Initialisation des états via StateManager
        StateManager.initialize_states()
        llm_state = StateManager.get_llm_state()
        
        # Sélection de l'API
        st.radio(
            "API LLM",
            options=['OpenAI', 'Anthropic'],
            index=0 if llm_state.selected_llm == 'OpenAI' else 1,
            horizontal=True,
            key='selected_llm',
            on_change=self.on_change
        )
        
        # Sélection du modèle en fonction de l'API
        current_llm = st.session_state.selected_llm
        models = self.OPENAI_MODELS.keys() if current_llm == 'OpenAI' else self.CLAUDE_MODELS.keys()
        
        st.selectbox(
            "Modèle",
            options=list(models),
            index=list(models).index(llm_state.selected_model) if llm_state.selected_model in models else 0,
            key='selected_model',
            on_change=self.on_change
        )
