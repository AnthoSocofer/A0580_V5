"""
Générateur de réponses pour l'interface de chat.
"""
from typing import List
from src.core.types import DocumentReference
from src.pages.components.llm.llm_selector import LLMSelector

class ChatResponseGenerator:
    """Générateur de réponses basées sur les sources documentaires."""
    
    def __init__(self):
        """Initialise le générateur de réponses."""
        self.llm_selector = LLMSelector()
    
    def generate_response(self, query: str, segments: List[DocumentReference]) -> str:
        """Génère une réponse basée sur les segments trouvés.
        
        Args:
            query: Question de l'utilisateur
            segments: Segments de documents pertinents
            
        Returns:
            Réponse générée
        """
        # Trier les segments par score de pertinence
        sorted_segments = sorted(segments, key=lambda x: x.relevance_score, reverse=True)
        
        # Préparation du contexte avec indication des sources
        context_parts = []
        for i, segment in enumerate(sorted_segments, 1):
            context = f"[Source {i}] {segment.text}"
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
            {"role": "user", "content": query}
        ]
        
        # Appel au LLM
        llm = self.llm_selector.get_llm()
        return llm.make_llm_call(messages)
