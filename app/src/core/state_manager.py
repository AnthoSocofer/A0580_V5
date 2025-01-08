"""
Gestionnaire centralisé des états Streamlit de l'application.
"""
import streamlit as st
from src.ui.states.chat_state import ChatState
from src.ui.states.llm_state import LLMState
from src.ui.states.kb_state import KBState
from src.ui.states.filter_state import KBFilterState, DocumentFilterState, FilterState

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
            kb_state = KBState()
            kb_state.filter_state = KBFilterState()
            st.session_state.kb_state = kb_state
            
        # Filter states
        if 'filter_state' not in st.session_state:
            filter_state = FilterState()
            filter_state.kb_filter = KBFilterState()
            filter_state.document_filter = DocumentFilterState()
            st.session_state.filter_state = filter_state
    
    @staticmethod
    def get_chat_state() -> ChatState:
        """Récupère l'état du chat."""
        return st.session_state.chat_state
    
    @staticmethod
    def get_llm_state() -> LLMState:
        """Récupère l'état du LLM."""
        return st.session_state.llm_state
    
    @staticmethod
    def get_kb_state() -> KBState:
        """Récupère l'état des bases de connaissances."""
        return st.session_state.kb_state
    
    @staticmethod
    def get_filter_state() -> FilterState:
        """Récupère l'état des filtres."""
        return st.session_state.filter_state
    
    @staticmethod
    def update_chat_state(chat_state: ChatState):
        """Met à jour l'état du chat."""
        st.session_state.chat_state = chat_state
    
    @staticmethod
    def update_llm_state(llm_state: LLMState):
        """Met à jour l'état du LLM."""
        st.session_state.llm_state = llm_state
    
    @staticmethod
    def update_kb_state(kb_state: KBState):
        """Met à jour l'état des bases de connaissances."""
        st.session_state.kb_state = kb_state
        
    @staticmethod
    def update_filter_state(filter_state: FilterState):
        """Met à jour l'état des filtres."""
        st.session_state.filter_state = filter_state
