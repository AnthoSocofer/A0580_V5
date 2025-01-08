"""
Gestion de l'état du sélecteur LLM.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMState:
    """État du sélecteur LLM."""
    selected_llm: str = "OpenAI"
    selected_model: str = "3.5-turbo"
    
    def reset(self):
        """Réinitialise l'état aux valeurs par défaut."""
        self.selected_llm = "OpenAI"
        self.selected_model = "3.5-turbo"
