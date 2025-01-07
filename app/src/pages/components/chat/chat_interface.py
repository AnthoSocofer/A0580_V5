"""
Interface de chat avec l'assistant.
"""
import streamlit as st
from typing import List
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.pages.components.chat.chat_source_manager import ChatSourceManager
from src.pages.components.chat.chat_response_generator import ChatResponseGenerator
from src.pages.components.chat.chat_search_manager import ChatSearchManager

class ChatInterface:
    """Interface de chat avec l'assistant."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise l'interface de chat."""
        self.kb_manager = kb_manager
        self.source_manager = ChatSourceManager(kb_manager)
        self.response_generator = ChatResponseGenerator()
        self.search_manager = ChatSearchManager(kb_manager)
        StateManager.initialize_states()
    
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
                            st.markdown(f"**Document**: {source['title']}")
                            if source.get("score"):
                                st.markdown(f"*Score de pertinence*: {source['score']:.2f}")
                            if source.get("pages"):
                                st.markdown(f"*{source['pages']}*")
                            if source.get("excerpt"):
                                st.markdown(f"*Extrait*:\n> {source['excerpt']}")
                            st.markdown(f"*Mode de recherche*: {source.get('search_mode', 'standard')}")
                            st.markdown("---")
        
        # Zone de saisie
        if prompt := st.chat_input("Votre message...", disabled=chat_state.is_processing):
            # Ajouter le message utilisateur
            chat_state.messages.append({
                "role": "user",
                "content": prompt
            })
            StateManager.update_chat_state(chat_state)
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Effectuer la recherche
            chat_state.is_processing = True
            StateManager.update_chat_state(chat_state)
            
            results = self.search_manager.perform_search(prompt)
            
            with st.chat_message("assistant"):
                if not results:
                    response_content = "Je n'ai trouvé aucun document pertinent."
                    st.markdown(response_content)
                else:
                    # Générer une réponse basée sur les sources
                    response_content = self.response_generator.generate_response(prompt, results)
                    st.markdown(response_content)
                    
                    # Afficher les sources détaillées
                    self.source_manager.render_sources(results, expanded=False)
                    # Afficher le résumé des sources principales
                    self.source_manager.render_source_summary(results)
            
            # Formater les sources pour le stockage
            sources = self.source_manager.format_sources(results)
            
            # Préparer et stocker la réponse
            response = {
                "role": "assistant",
                "content": response_content,
                "sources": sources
            }
            
            chat_state.messages.append(response)
            chat_state.is_processing = False
            chat_state.last_query = prompt
            chat_state.search_results = results
            
            # Mettre à jour l'état
            StateManager.update_chat_state(chat_state)
