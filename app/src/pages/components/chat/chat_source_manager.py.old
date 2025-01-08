"""
Gestionnaire des sources pour l'interface de chat.
"""
import streamlit as st
from typing import List, Dict, Any
from src.core.types import DocumentReference
from src.core.knowledge_bases_manager import KnowledgeBasesManager

class ChatSourceManager:
    """Gestionnaire pour l'affichage et le formatage des sources."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise le gestionnaire de sources.
        
        Args:
            kb_manager: Gestionnaire de bases de connaissances
        """
        self.kb_manager = kb_manager

    def format_sources(self, references: List[DocumentReference]) -> List[Dict[str, Any]]:
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
        
    def render_sources(self, segments: List[DocumentReference], expanded: bool = False):
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
    
    def render_source_summary(self, segments: List[DocumentReference]):
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
