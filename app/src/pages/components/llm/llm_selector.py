"""
Composant de sélection de l'API LLM.
"""
import streamlit as st
from dsrag.llm import OpenAIChatAPI, AnthropicChatAPI
from src.core.state_manager import StateManager
from src.pages.states.llm_state import LLMState

class LLMSelector:
    """Composant pour sélectionner l'API LLM à utiliser."""
    
    def __init__(self):
        """Initialise le sélecteur LLM."""
        self._setup_model_mappings()
        
    def _setup_model_mappings(self):
        """Configure les mappings des modèles."""
        self.CLAUDE_MODELS = {
            "haiku": "claude-3-haiku-20240307",
            "sonnet": "claude-3-sonnet-20240229",
            "opus": "claude-3-opus-20240229"
        }
        
        self.OPENAI_MODELS = {
            "3.5-turbo": "gpt-3.5-turbo",
            "4o-mini": "gpt-4o-mini",
            "4o": "gpt-4o"
        }
    
    def render(self):
        """Affiche l'interface de sélection du LLM."""
        llm_state = StateManager.get_llm_state()
        
        # Sélection du fournisseur LLM
        st.selectbox(
            "Fournisseur LLM",
            options=["OpenAI", "Anthropic"],
            key="selected_llm",
            on_change=self.on_change,
            index=0 if llm_state.selected_llm == "OpenAI" else 1
        )
        
        # Sélection du modèle en fonction du fournisseur
        models = list(self.OPENAI_MODELS.keys()) if llm_state.selected_llm == "OpenAI" else list(self.CLAUDE_MODELS.keys())
        st.selectbox(
            "Modèle",
            options=models,
            key="selected_model",
            on_change=self.on_change,
            index=models.index(llm_state.selected_model) if llm_state.selected_model in models else 0
        )
            
    def get_llm(self):
        """Retourne l'instance LLM appropriée basée sur la sélection."""
        llm_state = StateManager.get_llm_state()
        model = llm_state.selected_model
        
        if llm_state.selected_llm == 'OpenAI':
            full_model_name = self.OPENAI_MODELS.get(model, model)
            return OpenAIChatAPI(model=full_model_name)
        else:
            full_model_name = self.CLAUDE_MODELS.get(model, model)
            return AnthropicChatAPI(model=full_model_name)
            
    def on_change(self):
        """Gère les changements de sélection LLM ou modèle."""
        llm_state = StateManager.get_llm_state()
        current_llm = st.session_state.selected_llm
        current_model = st.session_state.selected_model
        
        if current_llm != llm_state.selected_llm:
            # Réinitialiser le modèle si le LLM change
            models = list(self.OPENAI_MODELS.keys()) if current_llm == "OpenAI" else list(self.CLAUDE_MODELS.keys())
            st.session_state.selected_model = models[0]
            current_model = models[0]
            
        # Mettre à jour l'état
        llm_state.selected_llm = current_llm
        llm_state.selected_model = current_model
