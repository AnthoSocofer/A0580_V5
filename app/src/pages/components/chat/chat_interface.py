"""
Interface de chat avec l'assistant.
"""
import streamlit as st
from typing import List, Dict, Any
from src.core.state_manager import StateManager
from src.core.search_engine import SearchEngine

class ChatInterface:
    """Interface de chat avec l'assistant."""
    
    def __init__(self):
        """Initialise l'interface de chat."""
        self.search_engine = SearchEngine()
    
    def _perform_search(self, query: str) -> List[Dict[str, Any]]:
        """Effectue une recherche documentaire.
        
        Args:
            query: Requête de recherche
            
        Returns:
            Liste des résultats de recherche
        """
        chat_state = StateManager.get_chat_state()
        
        # Effectuer la recherche dans les bases sélectionnées
        results = []
        if chat_state.selected_kbs:
            # Si des documents spécifiques sont sélectionnés, limiter la recherche à ces documents
            if chat_state.selected_docs:
                results = self.search_engine.search(
                    query=query,
                    kb_ids=chat_state.selected_kbs,
                    doc_ids=chat_state.selected_docs
                )
            else:
                # Sinon, rechercher dans toutes les bases sélectionnées
                results = self.search_engine.search(
                    query=query,
                    kb_ids=chat_state.selected_kbs
                )
        
        return results
    
    def render(self):
        """Affiche l'interface de chat."""
        st.markdown("## 💬 Discussion")
        
        chat_state = StateManager.get_chat_state()
        kb_state = StateManager.get_kb_state()
        
        if not kb_state.knowledge_bases:
            st.info("Aucune base de connaissances n'est disponible.")
            return
            
        if not chat_state.selected_kbs:
            st.info("Sélectionnez au moins une base de connaissances dans la barre latérale pour commencer.")
            return
            
        # Affichage des messages
        for message in chat_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Afficher les sources si présentes
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources", expanded=False):
                        for source in message["sources"]:
                            st.markdown(f"- {source['title']}")
                            if "excerpt" in source:
                                st.markdown(f"> {source['excerpt']}")
        
        # Zone de saisie
        if prompt := st.chat_input("Votre message...", disabled=chat_state.is_processing):
            # Ajouter le message utilisateur
            chat_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Effectuer la recherche
            chat_state.is_processing = True
            StateManager.update_chat_state(chat_state)
            
            results = self._perform_search(prompt)
            
            # Simuler une réponse de l'assistant avec les sources
            response = {
                "role": "assistant",
                "content": f"J'ai trouvé {len(results)} documents pertinents pour votre requête.",
                "sources": [{
                    "title": result["title"],
                    "excerpt": result.get("excerpt", "")
                } for result in results]
            }
            
            chat_state.messages.append(response)
            chat_state.is_processing = False
            
            # Mettre à jour l'état
            StateManager.update_chat_state(chat_state)
            
        # Indicateur de traitement
        if chat_state.is_processing:
            with st.chat_message("assistant"):
                st.write("En train de réfléchir...")
