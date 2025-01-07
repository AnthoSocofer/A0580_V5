"""
Interface de chat avec l'assistant.
"""
import streamlit as st
from typing import List, Dict, Any, Optional
from src.core.state_manager import StateManager
from src.core.search_engine import SearchEngine
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from src.core.types import DocumentReference
from src.pages.components.llm.llm_selector import LLMSelector

class ChatInterface:
    """Interface de chat avec l'assistant."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise l'interface de chat."""
        self.kb_manager = kb_manager
        self.search_engine = SearchEngine()
        self.llm_selector = LLMSelector()
        StateManager.initialize_states()
    
    def _perform_search(self, query: str) -> List[DocumentReference]:
        """Effectue une recherche documentaire.
        
        Args:
            query: Requête de recherche
            
        Returns:
            Liste des résultats de recherche
        """
        chat_state = StateManager.get_chat_state()
        
        # Récupérer les bases de connaissances actives
        knowledge_bases = []
        for kb_id in chat_state.selected_kbs:
            kb = self.kb_manager.get_knowledge_base(kb_id)
            if kb:
                knowledge_bases.append(kb)
        
        # Effectuer la recherche avec la nouvelle API
        try:
            results = self.search_engine.search_knowledge_bases(
                query=query,
                knowledge_bases=knowledge_bases,
                selected_kbs=chat_state.selected_kbs,
                selected_docs=chat_state.selected_docs
            )
            return results
        except Exception as e:
            st.error(f"Erreur lors de la recherche : {str(e)}")
            return []
    
    def _format_sources(self, references: List[DocumentReference]) -> List[Dict[str, Any]]:
        """Formate les références de documents pour l'affichage.
        
        Args:
            references: Liste des références de documents
            
        Returns:
            Liste des sources formatées pour l'affichage
        """
        sources = []
        for ref in references:
            # Récupérer les informations du document via le kb_manager
            docs = self.kb_manager.get_documents(ref.kb_id)
            doc_info = next(
                (doc for doc in docs if doc["doc_id"] == ref.doc_id),
                None
            )
            
            if not doc_info:
                continue
                
            source = {
                "title": doc_info.get("title", ref.doc_id),
                "excerpt": ref.text,
                "score": ref.relevance_score,
                "kb_id": ref.kb_id,
                "doc_id": ref.doc_id,
                "pages": f"Pages {ref.page_numbers[0]}-{ref.page_numbers[1]}" if ref.page_numbers[0] > 0 else "",
                "search_mode": ref.search_mode
            }
            sources.append(source)
        
        return sources
        
    def render_sources(self, segments, expanded=False):
        """Affiche les sources dans un expander.
        
        Args:
            segments: Liste des segments de documents
            expanded: Si True, l'expander est ouvert par défaut
        """
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
        """Affiche un résumé des sources principales.
        
        Args:
            segments: Liste des segments de documents
        """
        st.markdown("---")
        st.markdown("**Sources principales utilisées:**")
        for i, segment in enumerate(segments[:3], 1):
            if segment.relevance_score >= 0.5:  # Ne montrer que les sources pertinentes
                st.markdown(f"""
                - 📄 **Source {i}** ({segment.relevance_score:.2f}): {segment.doc_id} (p. {segment.page_numbers[0]}-{segment.page_numbers[1]})
                """)
    
    def _generate_response(self, query: str, segments: List[DocumentReference]) -> str:
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
            
            results = self._perform_search(prompt)
            
            with st.chat_message("assistant"):
                if not results:
                    response_content = "Je n'ai trouvé aucun document pertinent."
                    st.markdown(response_content)
                else:
                    # Générer une réponse basée sur les sources
                    response_content = self._generate_response(prompt, results)
                    st.markdown(response_content)
                    
                    # Afficher les sources détaillées
                    self.render_sources(results, expanded=False)
                    # Afficher le résumé des sources principales
                    self.render_source_summary(results)
            
            # Formater les sources pour le stockage
            sources = self._format_sources(results)
            
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
