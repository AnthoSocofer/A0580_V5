"""
Interface utilisateur pour la sélection de LLM.
"""
from typing import Optional
from src.ui.interfaces.ui_renderer import IUIRenderer
from src.ui.components.llm.business.llm_selector_logic import LLMSelectorLogic

class LLMSelectorUI:
    """Interface utilisateur pour la sélection de LLM."""
    
    def __init__(self, 
                 selector_logic: LLMSelectorLogic,
                 ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur."""
        self.selector_logic = selector_logic
        self.ui_renderer = ui_renderer
    
    def render(self) -> None:
        """Affiche l'interface de sélection du LLM."""
        current = self.selector_logic.get_current_selection()
        
        # Sélection du fournisseur
        provider = self.ui_renderer.render_select(
            label="Fournisseur LLM",
            options=self.selector_logic.get_providers(),
            default=current["provider"],
            on_change=lambda: self._on_provider_change()
        )
        
        # Sélection du modèle
        model = self.ui_renderer.render_select(
            label="Modèle",
            options=self.selector_logic.get_models_for_provider(provider),
            default=current["model"],
            on_change=lambda: self._on_model_change(provider)
        )
        
        # Mise à jour de l'état si nécessaire
        if provider != current["provider"] or model != current["model"]:
            self.selector_logic.update_selection(provider, model)
    
    def _on_provider_change(self) -> None:
        """Gestionnaire de changement de fournisseur."""
        current = self.selector_logic.get_current_selection()
        models = self.selector_logic.get_models_for_provider(current["provider"])
        if current["model"] not in models:
            self.selector_logic.update_selection(current["provider"], models[0])
    
    def _on_model_change(self, provider: str) -> None:
        """Gestionnaire de changement de modèle."""
        current = self.selector_logic.get_current_selection()
        if current["model"] != current["model"]:
            self.selector_logic.update_selection(provider, current["model"])
