"""
Gestionnaire centralisé des états Streamlit de l'application.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import streamlit as st

@dataclass
class ChatState:
    """État du chat."""
    messages: List[Dict[str, Any]] = field(default_factory=list)
    is_processing: bool = False

@dataclass
class LLMState:
    """État de la configuration LLM."""
    selected_llm: str = "OpenAI"
    selected_model: str = "3.5-turbo"

@dataclass
class KBState:
    """État de la gestion des bases de connaissances."""
    current_kb_metadata: Optional[Dict[str, Any]] = None
    current_kb_id: Optional[str] = None
    knowledge_bases_metadata: List[Dict[str, Any]] = field(default_factory=list)
    uploaded_files: Optional[List[Any]] = field(default_factory=list)
    active_expander: Optional[str] = None

class StateManager:
    """Gestionnaire centralisé des états de l'application."""
    
    @staticmethod
    def initialize_states():
        """Initialise tous les états s'ils n'existent pas déjà."""
        # Chat states
        if 'chat_state' not in st.session_state:
            st.session_state.chat_state = ChatState()
            
        # LLM states
        if 'llm_state' not in st.session_state:
            st.session_state.llm_state = LLMState()
            
        # KB states
        if 'kb_state' not in st.session_state:
            st.session_state.kb_state = KBState()
    
    @staticmethod
    def get_chat_state() -> ChatState:
        """Récupère l'état du chat."""
        return st.session_state.chat_state
    
    @staticmethod
    def update_chat_state(chat_state: ChatState) -> None:
        """Met à jour l'état du chat."""
        st.session_state.chat_state = chat_state
    
    @staticmethod
    def get_llm_state() -> LLMState:
        """Récupère l'état du LLM."""
        return st.session_state.llm_state
    
    @staticmethod
    def update_llm_state(llm_state: LLMState) -> None:
        """Met à jour l'état du LLM."""
        st.session_state.llm_state = llm_state
    
    @staticmethod
    def get_kb_state() -> KBState:
        """Récupère l'état des bases de connaissances."""
        return st.session_state.kb_state
    
    @staticmethod
    def update_kb_state(kb_state: KBState) -> None:
        """Met à jour l'état des bases de connaissances."""
        st.session_state.kb_state = kb_state
