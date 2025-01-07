"""
Composant pour la création d'une base de connaissances.
"""
import streamlit as st
from src.pages.components.kb.kb_operations import KBOperations

class KBCreator:
    """Composant pour la création d'une base de connaissances."""
    
    def __init__(self, kb_operations: KBOperations):
        """Initialise le créateur.
        
        Args:
            kb_operations: Opérations sur les bases de connaissances
        """
        self.kb_operations = kb_operations
    
    def render_form(self) -> None:
        """Affiche le formulaire de création d'une base."""
        with st.form("new_kb_form", clear_on_submit=True):
            kb_id = st.text_input(
                "ID de la base",
                placeholder="ma_base",
                help="Identifiant unique pour la base de connaissances"
            )
            kb_title = st.text_input(
                "Titre",
                placeholder="Ma Base de Connaissances",
                help="Titre descriptif de la base"
            )
            kb_description = st.text_area(
                "Description",
                placeholder="Description détaillée de la base...",
                help="Description du contenu et de l'usage de la base"
            )
            
            # Boutons côte à côte
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Créer")
            with col2:
                cancel_button = st.form_submit_button("Annuler")
            
            if submit_button:
                if not kb_id:
                    st.error("⚠️ L'ID de la base est requis!")
                elif not kb_title:
                    st.error("⚠️ Le titre de la base est requis!")
                else:
                    try:
                        self.kb_operations.create_knowledge_base(kb_id, kb_title, kb_description)
                        st.success(f"Base '{kb_title}' créée avec succès!")
                        st.session_state.show_kb_form = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur lors de la création de la base: {str(e)}")
            
            elif cancel_button:
                st.session_state.show_kb_form = False
                st.rerun()
