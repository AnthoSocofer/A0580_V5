"""
Logique métier pour la sélection de LLM.
"""
from typing import Dict, List, Any, Optional
from src.ui.interfaces.llm import ILLMSelector
from src.ui.interfaces.state_manager import IStateManager
from src.core.state_manager import StateManager
from dsrag.llm import OpenAIChatAPI, AnthropicChatAPI

class LLMSelectorLogic(ILLMSelector):
    """Logique métier pour la sélection de LLM."""
    
    def __init__(self, state_manager: Optional[IStateManager] = None):
        """Initialise la logique de sélection LLM."""
        self.state_manager = state_manager or StateManager
        self._setup_model_mappings()
        
    def _setup_model_mappings(self) -> None:
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
    
    def get_providers(self) -> List[str]:
        """Retourne la liste des fournisseurs disponibles."""
        return ["OpenAI", "Anthropic"]
    
    def get_models_for_provider(self, provider: str) -> List[str]:
        """Retourne la liste des modèles pour un fournisseur."""
        if provider == "OpenAI":
            return list(self.OPENAI_MODELS.keys())
        return list(self.CLAUDE_MODELS.keys())
    
    def get_current_selection(self) -> Dict[str, str]:
        """Retourne la sélection actuelle."""
        llm_state = self.state_manager.get_llm_state()
        return {
            "provider": llm_state.selected_llm,
            "model": llm_state.selected_model
        }
    
    def update_selection(self, provider: str, model: str) -> None:
        """Met à jour la sélection."""
        llm_state = self.state_manager.get_llm_state()
        
        # Si le fournisseur change, réinitialiser le modèle
        if provider != llm_state.selected_llm:
            models = self.get_models_for_provider(provider)
            model = models[0]
        
        llm_state.selected_llm = provider
        llm_state.selected_model = model
        self.state_manager.update_llm_state(llm_state)
    
    def get_llm(self) -> Any:
        """Retourne l'instance LLM appropriée."""
        current = self.get_current_selection()
        provider = current["provider"]
        model = current["model"]
        
        if provider == 'OpenAI':
            full_model_name = self.OPENAI_MODELS.get(model, model)
            return OpenAIChatAPI(model=full_model_name)
        else:
            full_model_name = self.CLAUDE_MODELS.get(model, model)
            return AnthropicChatAPI(model=full_model_name)
