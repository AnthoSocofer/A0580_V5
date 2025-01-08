"""
Générateur de réponses pour le chat.
"""
from typing import List, Dict, Any, Optional
from src.core.types import DocumentReference
from src.ui.interfaces.chat import IChatResponseGenerator
from src.ui.components.llm.business.llm_selector_logic import LLMSelectorLogic

class ChatResponseGenerator(IChatResponseGenerator):
    """Générateur de réponses basées sur les sources documentaires."""
    
    def __init__(self):
        """Initialise le générateur de réponses."""
        self.llm_selector = LLMSelectorLogic()
    
    def generate_response(self, 
                         prompt: str,
                         context: Optional[List[Dict[str, Any]]] = None) -> str:
        """Génère une réponse basée sur le contexte.
        
        Args:
            prompt: Question de l'utilisateur
            context: Segments de documents pertinents
            
        Returns:
            str: Réponse générée
        """
        if not context:
            return "Je n'ai trouvé aucun document pertinent."
            
        # Trier les segments par score de pertinence
        sorted_segments = sorted(context, key=lambda x: x.get('score', 0), reverse=True)
        
        # Préparation du contexte avec indication des sources
        context_parts = []
        for i, segment in enumerate(sorted_segments, 1):
            text = segment.get('text', '')
            context = f"[Source {i}] {text}"
            context_parts.append(context)
        
        # Préparation de la réponse
        context_text = "\n\n".join(context_parts)
        system_prompt = f"""Tu es un assistant documentaire expert. Réponds à la question en te basant uniquement sur les sources fournies.
        Cite tes sources en utilisant les numéros entre crochets [Source X].
        Si tu ne trouves pas l'information dans les sources, dis-le clairement.
        
        Sources:
        {context_text}
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        # Appel au LLM
        llm = self.llm_selector.get_llm()
        return llm.make_llm_call(messages)
