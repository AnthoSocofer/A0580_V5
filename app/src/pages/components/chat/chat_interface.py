"""
Interface de chat avec l'assistant.
"""
import streamlit as st
from typing import List, Dict, Any
from src.core.state_manager import StateManager

class ChatInterface:
    """Interface de chat avec l'assistant."""
    
    def render(self):
        """Affiche l'interface de chat."""
        st.markdown("## 💬 Discussion")
        
        chat_state = StateManager.get_chat_state()
        kb_state = StateManager.get_kb_state()
        
        if not kb_state.current_kb_metadata:
            st.info("Sélectionnez une base de connaissances dans la barre latérale pour commencer.")
            return
            
        # Affichage des messages
        for message in chat_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Zone de saisie
        if prompt := st.chat_input("Votre message...", disabled=chat_state.is_processing):
            # Ajouter le message utilisateur
            chat_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Simuler une réponse de l'assistant
            chat_state.messages.append({
                "role": "assistant",
                "content": f"Vous avez dit : {prompt}"
            })
            
            # Mettre à jour l'état
            StateManager.update_chat_state(chat_state)
            
        # Indicateur de traitement
        if chat_state.is_processing:
            with st.chat_message("assistant"):
                st.write("En train de réfléchir...")
