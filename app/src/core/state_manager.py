"""
Gestionnaire centralisé des états Streamlit de l'application.
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import streamlit as st
from dsrag.knowledge_base import KnowledgeBase

@dataclass
class ChatState:
    """État du chat."""
    messages: List[Dict[str, Any]] = None
    selected_kbs: List[str] = None  
    selected_docs: List[str] = None
    kb_filter_initialized: bool = False
    kb_options: Dict[str, str] = None
    selected_kb_titles: List[str] = None
    cached_documents: Dict[str, List[Dict[str, Any]]] = None

@dataclass
class LLMState:
    """État de la configuration LLM."""
    selected_llm: str = "OpenAI"
    selected_model: str = "3.5-turbo"

@dataclass
class KBState:
    """État de la gestion des bases de connaissances."""
    current_kb: Optional[KnowledgeBase] = None
    current_kb_id: Optional[str] = None
    active_expander: Optional[str] = None
    knowledge_bases: List[Dict[str, Any]] = None

class StateManager:
    """Gestionnaire centralisé des états de l'application."""
    
    @staticmethod
    def initialize_states():
        """Initialise tous les états s'ils n'existent pas déjà."""
        # Chat states
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'selected_kbs' not in st.session_state:
            st.session_state.selected_kbs = []
        if 'selected_docs' not in st.session_state:
            st.session_state.selected_docs = []
        if 'kb_filter_initialized' not in st.session_state:
            st.session_state.kb_filter_initialized = False
        if 'kb_options' not in st.session_state:
            st.session_state.kb_options = {}
        if 'selected_kb_titles' not in st.session_state:
            st.session_state.selected_kb_titles = []
        if 'cached_documents' not in st.session_state:
            st.session_state.cached_documents = {}
        if 'knowledge_bases' not in st.session_state:
            st.session_state.knowledge_bases = []

        # LLM states
        if 'selected_llm' not in st.session_state:
            st.session_state.selected_llm = 'OpenAI'
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = '3.5-turbo'

        # KB states
        if 'current_kb' not in st.session_state:
            st.session_state.current_kb = None
        if 'current_kb_id' not in st.session_state:
            st.session_state.current_kb_id = None
        if 'active_expander' not in st.session_state:
            st.session_state.active_expander = None

    @staticmethod
    def get_chat_state() -> ChatState:
        """Récupère l'état du chat."""
        return ChatState(
            messages=st.session_state.messages,
            selected_kbs=st.session_state.selected_kbs,
            selected_docs=st.session_state.selected_docs,
            kb_filter_initialized=st.session_state.kb_filter_initialized,
            kb_options=st.session_state.kb_options,
            selected_kb_titles=st.session_state.selected_kb_titles,
            cached_documents=st.session_state.cached_documents
        )

    @staticmethod
    def get_llm_state() -> LLMState:
        """Récupère l'état de la configuration LLM."""
        return LLMState(
            selected_llm=st.session_state.selected_llm,
            selected_model=st.session_state.selected_model
        )

    @staticmethod
    def update_llm_state(state: LLMState):
        """Met à jour l'état de la configuration LLM."""
        st.session_state.selected_llm = state.selected_llm
        st.session_state.selected_model = state.selected_model

    @staticmethod
    def get_kb_state() -> KBState:
        """Récupère l'état de la gestion des bases."""
        return KBState(
            current_kb=st.session_state.current_kb,
            current_kb_id=st.session_state.current_kb_id,
            active_expander=st.session_state.active_expander,
            knowledge_bases=st.session_state.knowledge_bases
        )

    @staticmethod
    def update_kb_state(state: KBState):
        """Met à jour l'état de la gestion des bases."""
        st.session_state.current_kb = state.current_kb
        st.session_state.current_kb_id = state.current_kb_id
        st.session_state.active_expander = state.active_expander
        st.session_state.knowledge_bases = state.knowledge_bases or []

    @staticmethod
    def update_chat_state(state: ChatState):
        """Met à jour l'état du chat."""
        st.session_state.messages = state.messages or []
        st.session_state.selected_kbs = state.selected_kbs or []
        st.session_state.selected_docs = state.selected_docs or []
        st.session_state.kb_filter_initialized = state.kb_filter_initialized
        st.session_state.kb_options = state.kb_options or {}
        st.session_state.selected_kb_titles = state.selected_kb_titles or []
        st.session_state.cached_documents = state.cached_documents or {}

    @staticmethod
    def clear_chat_state():
        """Réinitialise l'état du chat."""
        st.session_state.messages = []
        st.session_state.selected_kbs = []
        st.session_state.selected_docs = []
        st.session_state.kb_filter_initialized = False
        st.session_state.kb_options = {}
        st.session_state.selected_kb_titles = []
        st.session_state.cached_documents = {}
