"""
Page de chat avec l'assistant.
"""
import streamlit as st
from typing import Dict, Any, List
from src.core.state_manager import StateManager
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.types import KnowledgeBase, Document, DocumentReference
from src.pages.components.llm_selector import LLMSelector
from src.core.search_engine import SearchEngine

class ChatPage:
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise la page de chat.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
        self.search_engine = SearchEngine()
        self.llm_selector = LLMSelector()
        StateManager.initialize_states()
    
    def handle_kb_selection(self, selected_kbs: List[str]):
        """Gère la sélection des bases de connaissances"""
        chat_state = StateManager.get_chat_state()
        chat_state.selected_kbs = selected_kbs
        if not selected_kbs:  # Si aucune base sélectionnée, vider aussi la sélection des documents
            chat_state.selected_docs = []
        StateManager.update_chat_state(chat_state)
    
    def handle_doc_selection(self, selected_docs: List[str]):
        """Gère la sélection des documents"""
        chat_state = StateManager.get_chat_state()
        chat_state.selected_docs = selected_docs
        StateManager.update_chat_state(chat_state)
    
    def render_filters(self, knowledge_bases: List[Dict[str, Any]], key_prefix: str = ""):
        """Affiche les filtres de recherche dans la sidebar.
        
        Args:
            knowledge_bases: Liste des bases de connaissances
            key_prefix: Préfixe pour les clés des composants Streamlit
        """
        # Filtre des bases de connaissances
        st.markdown("### Bases de connaissances")
        
        chat_state = StateManager.get_chat_state()
        
        # Initialiser ou mettre à jour les options si nécessaire
        if not chat_state.kb_options or len(chat_state.kb_options) != len(knowledge_bases):
            chat_state.kb_options = {
                kb.get('title', kb['kb_id']): kb['kb_id']
                for kb in knowledge_bases
            }
            # Réinitialiser les sélections si les options ont changé
            chat_state.selected_kb_titles = list(chat_state.kb_options.keys())
            chat_state.selected_kbs = list(chat_state.kb_options.values())
            chat_state.kb_filter_initialized = True
            chat_state.cached_documents = {}
            StateManager.update_chat_state(chat_state)
        
        # Afficher le sélecteur de bases de connaissances
        selected_kb_titles = st.multiselect(
            "Bases de connaissances",
            options=list(chat_state.kb_options.keys()),
            default=chat_state.selected_kb_titles,
            key=f"{key_prefix}kb_selector"
        )
        
        # Mise à jour des sélections si changées
        if selected_kb_titles != chat_state.selected_kb_titles:
            chat_state.selected_kb_titles = selected_kb_titles
            chat_state.selected_kbs = [chat_state.kb_options[title] for title in selected_kb_titles]
            chat_state.selected_docs = []
            chat_state.cached_documents = {}
            StateManager.update_chat_state(chat_state)
        
        # Filtre des documents
        if chat_state.selected_kbs:
            st.markdown("### Documents")
            
            # Initialiser ou mettre à jour le cache des documents
            if not chat_state.cached_documents:
                chat_state.cached_documents = {}
                for kb_id in chat_state.selected_kbs:
                    if kb_id not in chat_state.cached_documents:
                        docs = self.kb_manager.list_documents(kb_id)
                        chat_state.cached_documents[kb_id] = docs
                StateManager.update_chat_state(chat_state)
            
            # Construire la liste des documents disponibles
            all_docs = []
            for kb_id in chat_state.selected_kbs:
                docs = chat_state.cached_documents.get(kb_id, [])
                for doc in docs:
                    doc_title = doc.get('title', doc['doc_id'])
                    if isinstance(doc_title, dict) and 'title' in doc_title:
                        doc_title = doc_title['title']
                    doc.update({
                        'kb_id': kb_id,
                        'title': f"{doc_title} ({kb_id})"  # Ajouter l'ID de la base pour l'unicité
                    })
                    all_docs.append(doc)
            
            # Créer les options de documents
            doc_options = {doc['title']: doc['doc_id'] for doc in all_docs}
            
            # Sélection des documents
            selected_doc_titles = st.multiselect(
                "Sélectionner les documents",
                options=list(doc_options.keys()),
                default=[title for title, doc_id in doc_options.items() if doc_id in chat_state.selected_docs],
                key=f"{key_prefix}_doc_multiselect"
            )
            
            # Mettre à jour la sélection des documents seulement si elle a changé
            new_selected_docs = [doc_options[title] for title in selected_doc_titles]
            if new_selected_docs != chat_state.selected_docs:
                chat_state.selected_docs = new_selected_docs
                StateManager.update_chat_state(chat_state)
    
    def render_sources(self, segments, expanded=False):
        """Affiche les sources dans un expander"""
        with st.expander("📚 Voir toutes les sources en détail", expanded=expanded):
            st.markdown("### Documents pertinents trouvés")
            
            for i, segment in enumerate(segments, 1):
                # Définir la couleur en fonction du score
                if segment.relevance_score >= 0.8:
                    color = "🟢"  # Très pertinent
                elif segment.relevance_score >= 0.6:
                    color = "🟡"  # Moyennement pertinent
                else:
                    color = "🔴"  # Peu pertinent
                
                # Créer un container pour chaque source
                with st.container():
                    # En-tête avec score et métadonnées
                    header_cols = st.columns([1, 2, 2])
                    with header_cols[0]:
                        st.markdown(f"**Source {i}**  \n{color}")
                        st.markdown(f"Score: **{segment.relevance_score:.2f}**")
                    with header_cols[1]:
                        st.markdown(f"""
                        **Document**: {segment.doc_id}  
                        **Base**: {segment.kb_id}
                        """)
                    with header_cols[2]:
                        st.markdown(f"""
                        **Pages**: {segment.page_numbers[0]}-{segment.page_numbers[1]}  
                        """)
                        
                    # Contenu du segment dans un bloc de code
                    st.code(segment.text, language="text")
                    st.divider()
    
    def render_source_summary(self, segments):
        """Affiche un résumé des sources principales"""
        st.markdown("---")
        st.markdown("**Sources principales utilisées:**")
        for i, segment in enumerate(segments[:3], 1):
            if segment.relevance_score >= 0.5:  # Ne montrer que les sources pertinentes
                st.markdown(f"""
                - 📄 **Source {i}** ({segment.relevance_score:.2f}): {segment.doc_id} (p. {segment.page_numbers[0]}-{segment.page_numbers[1]})
                """)
    
    def render(self):
        """Affiche l'interface de chat"""
        st.title("Assistant de Recherche Documentaire")
        
        # Affichage de l'historique des messages
        for message in StateManager.get_chat_state().messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Zone de saisie du message
        if query := st.chat_input("Posez votre question..."):
            if not StateManager.get_chat_state().selected_kbs:
                st.error("Aucune base de connaissances sélectionnée!")
                return
                
            # Affichage du message utilisateur
            StateManager.get_chat_state().messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)
            
            # Récupération des bases de connaissances sélectionnées
            knowledge_bases = []
            for kb_id in StateManager.get_chat_state().selected_kbs:
                kb = self.kb_manager.get_knowledge_base(kb_id)
                if kb:
                    knowledge_bases.append(kb)
                    
            if not knowledge_bases:
                st.error("Aucune base de connaissances valide sélectionnée!")
                return
                
            # Recherche dans toutes les bases
            relevant_segments = self.search_engine.search_knowledge_bases(
                query=query,
                knowledge_bases=knowledge_bases,
                selected_kbs=StateManager.get_chat_state().selected_kbs,
                selected_docs=StateManager.get_chat_state().selected_docs
            )
            print('relevant_segments', relevant_segments)
            # Préparation du contexte avec indication des sources
            context_parts = []
            sorted_segments = sorted(relevant_segments, key=lambda x: x.relevance_score, reverse=True)
            
            # Préparation des segments pour le contexte
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
            
            # Appel à l'API OpenAI
            llm = self.llm_selector.get_llm()
            answer = llm.make_llm_call(messages)
            
            # Affichage de la réponse
            StateManager.get_chat_state().messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
                self.render_source_summary(sorted_segments)
                self.render_sources(sorted_segments)
