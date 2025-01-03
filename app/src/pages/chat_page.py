"""
Page de chat avec l'assistant documentaire.
"""
import streamlit as st
from typing import List, Dict, Any
from dsrag.knowledge_base import KnowledgeBase
from dsrag.llm import OpenAIChatAPI
from src.core.search_engine import SearchEngine, DocumentReference
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class ChatPage:
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise la page de chat.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager
        self.search_engine = SearchEngine()
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'selected_kbs' not in st.session_state:
            st.session_state.selected_kbs = []
        if 'selected_docs' not in st.session_state:
            st.session_state.selected_docs = []
        if 'kb_filter_initialized' not in st.session_state:
            st.session_state.kb_filter_initialized = False
    
    def handle_kb_selection(self, selected_kbs: List[str]):
        """Gère la sélection des bases de connaissances"""
        st.session_state.selected_kbs = selected_kbs
        if not selected_kbs:  # Si aucune base sélectionnée, vider aussi la sélection des documents
            st.session_state.selected_docs = []
    
    def handle_doc_selection(self, selected_docs: List[str]):
        """Gère la sélection des documents"""
        st.session_state.selected_docs = selected_docs
    
    def render_filters(self, knowledge_bases: List[Dict[str, Any]], key_prefix: str = ""):
        """Affiche les filtres de recherche dans la sidebar
        
        Args:
            knowledge_bases: Liste des bases de connaissances
            key_prefix: Préfixe pour les clés des composants Streamlit
        """
        # Filtre des bases de connaissances
        st.markdown("### Bases de connaissances")
        kb_options = {}
        for kb in knowledge_bases:
            title = kb.get('title', kb['kb_id'])
            kb_options[title] = kb['kb_id']
            
        selected_kb_titles = st.multiselect(
            "Sélectionnez les bases de connaissances à interroger",
            options=list(kb_options.keys()),
            default=list(kb_options.keys()) if not st.session_state.kb_filter_initialized else None,
            key=f"{key_prefix}filter_kb_select"
        )
        st.session_state.selected_kbs = [kb_options[title] for title in selected_kb_titles]
        st.session_state.kb_filter_initialized = True
        
        # Filtre des documents
        if st.session_state.selected_kbs:
            st.markdown("### Documents")
            all_docs = []
            for kb_id in st.session_state.selected_kbs:
                docs = self.kb_manager.list_documents(kb_id)
                for doc in docs:
                    doc_title = doc.get('title', doc['doc_id'])
                    if isinstance(doc_title, dict) and 'title' in doc_title:
                        doc_title = doc_title['title']
                    doc.update({
                        'kb_id': kb_id,
                        'title': doc_title
                    })
                    all_docs.append(doc)
            
            doc_options = {doc['title']: doc['doc_id'] for doc in all_docs}
            selected_doc_titles = st.multiselect(
                "Sélectionner les documents",
                options=list(doc_options.keys()),
                default=[title for title, doc_id in doc_options.items() if doc_id in st.session_state.selected_docs],
                key=f"{key_prefix}filter_doc_select"
            )
            st.session_state.selected_docs = [doc_options[title] for title in selected_doc_titles]
    
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
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Zone de saisie du message
        if query := st.chat_input("Posez votre question..."):
            if not st.session_state.selected_kbs:
                st.error("Aucune base de connaissances sélectionnée!")
                return
                
            # Affichage du message utilisateur
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)
            
            # Récupération des bases de connaissances sélectionnées
            knowledge_bases = []
            for kb_id in st.session_state.selected_kbs:
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
                selected_kbs=st.session_state.selected_kbs,
                selected_docs=st.session_state.selected_docs
            )
            
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
            llm = OpenAIChatAPI()
            answer = llm.make_llm_call(messages)
            
            # Affichage de la réponse
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
                self.render_source_summary(sorted_segments)
                self.render_sources(sorted_segments)
