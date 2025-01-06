"""
Page de gestion des bases de connaissances.
"""
import streamlit as st
import tempfile
import os
import logging
from typing import List
from src.core.knowledge_bases_manager import KnowledgeBasesManager
from dsrag.knowledge_base import KnowledgeBase
from src.pages import components

class KnowledgeBasePage:
    """Page de gestion des bases de connaissances."""
    
    def __init__(self, kb_manager: KnowledgeBasesManager):
        """Initialise la page avec le gestionnaire de bases."""
        self.kb_manager = kb_manager
        self.logger = logging.getLogger(__name__)
        if 'current_kb' not in st.session_state:
            st.session_state.current_kb = None
        if 'active_expander' not in st.session_state:
            st.session_state.active_expander = None
        if 'current_kb_id' not in st.session_state:
            st.session_state.current_kb_id = None

    def handle_kb_creation(self, kb_id: str, title: str, description: str):
        """Gère la création d'une base de connaissances."""
        try:
            kb = self.kb_manager.create_knowledge_base(
                kb_id=kb_id,
                title=title,
                description=description,
                exists_ok=True
            )
            st.session_state.current_kb = kb
            st.session_state.current_kb_id = kb_id
            st.success(f"Base '{title}' créée avec succès!")
        except Exception as e:
            st.error(f"Erreur lors de la création: {str(e)}")
    
    def handle_kb_selection(self, kb_id: str):
        """Gère la sélection d'une base de connaissances."""
        if kb_id == st.session_state.get('current_kb_id'):  # Évite les rechargements inutiles
            return
            
        try:
            kb = self.kb_manager.get_knowledge_base(kb_id)
            if kb:
                st.session_state.current_kb = kb
                st.session_state.current_kb_id = kb_id
            else:
                st.error(f"Erreur lors du chargement de la base {kb_id}")
        except Exception as e:
            st.error(f"Erreur lors du chargement: {str(e)}")
    
    def handle_document_upload(self, files: List[tempfile.NamedTemporaryFile]):
        """Gère l'upload de documents."""
        for uploaded_file in files:
            self.logger.info(f"Début du traitement du fichier: {uploaded_file.name}")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                try:
                    # Écrire le contenu du fichier uploadé dans un fichier temporaire
                    self.logger.debug(f"Création du fichier temporaire: {tmp_file.name}")
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file.flush()  # S'assurer que tout est écrit
                    self.logger.debug(f"Fichier temporaire créé avec succès: {tmp_file.name}")
                    
                    kb = st.session_state.current_kb
                    if not kb:
                        self.logger.error("Aucune base de connaissances sélectionnée")
                        st.error("Veuillez sélectionner une base de connaissances")
                        return

                    self.logger.info(f"Ajout du document à la base {kb.kb_id}")
                    kb.add_document(
                        doc_id=uploaded_file.name,
                        file_path=tmp_file.name,  # Utiliser le chemin du fichier temporaire
                        document_title=uploaded_file.name,
                        auto_context_config={
                            "use_generated_title": False,  # Disable generated titles
                            "get_document_summary": True,  # Enable document summaries
                            "get_section_summaries": True  # Enable section summaries
                        }
                    )
                    self.logger.info(f"Document {uploaded_file.name} ajouté avec succès à la base {kb.kb_id}")
                    st.success(f"Document {uploaded_file.name} ajouté avec succès!")
                    
                    # Utiliser un flag pour indiquer que le fichier a été traité
                    upload_key = f"upload_{kb.kb_id}"
                    processed_key = f"processed_{upload_key}"
                    
                    if processed_key not in st.session_state:
                        st.session_state[processed_key] = set()
                    
                    st.session_state[processed_key].add(uploaded_file.name)
                    
                    # Mettre à jour la liste des bases
                    if 'knowledge_bases' in st.session_state:
                        self.logger.debug("Rechargement de la liste des bases de connaissances")
                        st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
                    
                    # Recharger la page une seule fois
                    st.rerun()
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'ajout du document {uploaded_file.name}: {str(e)}")
                    st.error(f"Erreur lors de l'ajout du document {uploaded_file.name}: {str(e)}")
                finally:
                    try:
                        # S'assurer que le fichier temporaire est fermé et supprimé
                        self.logger.debug(f"Nettoyage du fichier temporaire: {tmp_file.name}")
                        tmp_file.close()
                        os.unlink(tmp_file.name)
                        self.logger.debug("Fichier temporaire supprimé avec succès")
                    except Exception as e:
                        self.logger.error(f"Erreur lors de la suppression du fichier temporaire: {str(e)}")
    
    def handle_expander_change(self, kb_id: str, is_expanded: bool):
        """Gère le changement d'état d'un expander."""
        if is_expanded:
            if st.session_state.active_expander != kb_id:
                st.session_state.active_expander = kb_id
                self.handle_kb_selection(kb_id)
        elif st.session_state.active_expander == kb_id:
            st.session_state.active_expander = None
            st.session_state.current_kb = None
            st.session_state.current_kb_id = None
    
    def handle_document_delete(self, kb_id: str, doc_id: str):
        """Gère la suppression d'un document."""
        try:
            self.kb_manager.delete_document(kb_id, doc_id)
            st.success(f"Document {doc_id} supprimé")
            # Forcer le rechargement des documents
            if 'knowledge_bases' in st.session_state:
                st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {str(e)}")

    def render(self):
        """Affiche la page de gestion des bases de connaissances."""
        
        st.title("Gestion des Bases de Connaissances")
        
        # Création d'une nouvelle base
        with st.expander("Créer une nouvelle base", expanded=False):
            components.create_knowledge_base_form(self.handle_kb_creation)
        
        # Bases disponibles
        st.markdown("### Bases disponibles")
        
        # Utiliser la liste des bases stockée dans la session
        if 'knowledge_bases' not in st.session_state:
            st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
        
        for kb in st.session_state.knowledge_bases:
            kb_id = kb['kb_id']
            is_active = kb_id == st.session_state.active_expander
            
            # Utiliser un ID unique pour le titre de l'expander
            unique_title = f"{kb.get('title', kb_id)} ({kb_id})"
            expander = st.expander(unique_title, expanded=is_active)
            
            with expander:
                st.markdown(f"**ID**: {kb_id}")
                if kb.get('description'):
                    st.markdown(f"**Description**: {kb['description']}")
                
                # Si l'expander change d'état
                if expander.expanded != is_active:
                    self.handle_expander_change(kb_id, expander.expanded)
                
                # Afficher les fonctionnalités si l'expander est actif
                if expander.expanded:
                    st.markdown("---")
                    
                    # Upload de documents
                    st.markdown("#### Ajouter des documents")
                    
                    # Clé unique pour le widget d'upload
                    upload_key = f"upload_{kb_id}"
                    processed_key = f"processed_{upload_key}"
                    
                    if processed_key not in st.session_state:
                        st.session_state[processed_key] = set()
                    
                    uploaded_files = st.file_uploader(
                        "Sélectionner des fichiers PDF",
                        type=['pdf'],
                        accept_multiple_files=True,
                        key=upload_key
                    )
                    
                    if uploaded_files:
                        # Identifier les fichiers non traités
                        new_files = [
                            f for f in uploaded_files 
                            if f.name not in st.session_state[processed_key]
                        ]
                        
                        if new_files:
                            self.handle_document_upload(new_files)
                    
                    # Liste des documents
                    st.markdown("#### Documents disponibles")
                    try:
                        documents = self.kb_manager.list_documents(kb_id)
                        if documents:
                            # Créer des colonnes pour chaque ligne de document
                            for doc in documents:
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    doc_title = doc.get('title', doc['doc_id'])
                                    if isinstance(doc_title, dict) and 'title' in doc_title:
                                        doc_title = doc_title['title']
                                    st.text(doc_title)
                                with col2:
                                    if st.button("🗑️", key=f"delete_{kb_id}_{doc['doc_id']}"):
                                        self.handle_document_delete(kb_id, doc['doc_id'])
                        else:
                            st.info("Aucun document")
                    except Exception as e:
                        st.error(f"Erreur lors de la liste des documents: {str(e)}")
                    
                    st.markdown("---")
                    
                    # Bouton de suppression de la base
                    if st.button("Supprimer la base", key=f"delete_kb_{kb_id}"):
                        if self.kb_manager.delete_knowledge_base(kb_id):
                            st.success(f"Base {kb_id} supprimée")
                            st.session_state.active_expander = None
                            st.session_state.current_kb = None
                            st.session_state.current_kb_id = None
                            if 'knowledge_bases' in st.session_state:
                                st.session_state.knowledge_bases = self.kb_manager.list_knowledge_bases()
                            st.rerun()
