"""
Interface utilisateur pour la gestion des bases de connaissances.
"""
from typing import Optional, List
from src.pages.interfaces.ui_renderer import IUIRenderer
from src.pages.components.kb.domain.kb_manager_logic import KBManagerLogic

class KBManagerUI:
    """Interface utilisateur pour la gestion des bases de connaissances."""
    
    def __init__(self,
                 kb_logic: KBManagerLogic,
                 ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur."""
        self.kb_logic = kb_logic
        self.ui_renderer = ui_renderer
    
    def render(self) -> None:
        """Affiche l'interface de gestion des bases de connaissances."""
        # Liste des bases
        self._render_kb_list()
    
    def _render_kb_list(self) -> None:
        """Affiche la liste des bases de connaissances."""
        knowledge_bases = self.kb_logic.list_knowledge_bases()
        
        if not knowledge_bases:
            self.ui_renderer.render_info("Aucune base de connaissances disponible")
            return
        
        for idx, kb in enumerate(knowledge_bases):
            with self.ui_renderer.expander(f" {kb.title} ({kb.id})", expanded=False):
                # Description
                if kb.description:
                    self.ui_renderer.render_markdown(f"**Description**: {kb.description}")
                
                # Section ajout de documents
                self.ui_renderer.render_markdown("### Ajouter des documents")
                
                # Zone de drag & drop
                uploaded_files = self.ui_renderer.render_file_uploader(
                    "Drag and drop files here",
                    key=f"file_uploader_{kb.id}",
                    accept_multiple_files=True,
                    help="Limit 200MB per file"
                )
                
                # Traitement des fichiers uploadés
                if uploaded_files:
                    for file in uploaded_files:
                        if self.kb_logic.add_document(kb.id, file):
                            self.ui_renderer.render_success(f"Document {file.name} ajouté")
                        else:
                            self.ui_renderer.render_error(
                                f"Erreur lors de l'ajout de {file.name}"
                            )
                
                # Liste des documents
                self.ui_renderer.render_markdown("### Documents")
                
                if not kb.documents:
                    self.ui_renderer.render_info("Aucun document disponible")
                else:
                    for doc in kb.documents:
                        # Ligne avec document et bouton de suppression
                        col1, col2 = self.ui_renderer.columns([0.9, 0.1])
                        with col1:
                            self.ui_renderer.render_markdown(f" {doc.filename}")
                        with col2:
                            if self.ui_renderer.render_button(
                                "",
                                key=f"delete_doc_button_{kb.id}_{doc.filename}"
                            ):
                                if self.kb_logic.delete_document(kb.id, doc.filename):
                                    self.ui_renderer.render_success("Document supprimé")
                                else:
                                    self.ui_renderer.render_error(
                                        "Erreur lors de la suppression"
                                    )
                
                # Bouton de suppression de la base en bas
                self.ui_renderer.render_markdown("---")
                if self.ui_renderer.render_button(
                    " Supprimer base de connaissances",
                    key=f"delete_kb_button_{kb.id}"
                ):
                    if self.kb_logic.delete_knowledge_base(kb.id):
                        self.ui_renderer.render_success("Base supprimée")
                    else:
                        self.ui_renderer.render_error(
                            "Erreur lors de la suppression"
                        )
