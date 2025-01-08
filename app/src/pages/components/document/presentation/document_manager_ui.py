"""
Interface utilisateur pour la gestion des documents.
"""
from typing import Optional, BinaryIO
from src.pages.interfaces.ui_renderer import IUIRenderer
from src.pages.components.document.domain.document_manager_logic import DocumentManagerLogic

class DocumentManagerUI:
    """Interface utilisateur pour la gestion des documents."""
    
    def __init__(self,
                 document_logic: DocumentManagerLogic,
                 ui_renderer: IUIRenderer):
        """Initialise l'interface utilisateur."""
        self.document_logic = document_logic
        self.ui_renderer = ui_renderer
    
    def render(self, kb_id: str) -> None:
        """Affiche l'interface de gestion des documents."""
        self.ui_renderer.render_markdown("## 📄 Documents")
        
        # Affichage des extensions supportées
        extensions = self.document_logic.get_supported_extensions()
        self.ui_renderer.render_info(
            f"Extensions supportées : {', '.join(extensions)}"
        )
        
        # Zone de téléchargement
        uploaded_file = self.ui_renderer.render_file_uploader(
            "Télécharger un document",
            accepted_types=extensions
        )
        
        if uploaded_file:
            self._handle_file_upload(uploaded_file, kb_id)
        
        # Liste des documents
        self._render_document_list(kb_id)
    
    def _handle_file_upload(self, file: BinaryIO, kb_id: str) -> None:
        """Gère le téléchargement d'un fichier."""
        document_id = self.document_logic.upload_document(file, kb_id)
        if document_id:
            self.ui_renderer.render_success(
                f"Document téléchargé avec succès (ID: {document_id})"
            )
        else:
            self.ui_renderer.render_error(
                "Erreur lors du téléchargement du document"
            )
    
    def _render_document_list(self, kb_id: str) -> None:
        """Affiche la liste des documents."""
        documents = self.document_logic.list_documents(kb_id)
        
        if not documents:
            self.ui_renderer.render_info("Aucun document disponible")
            return
        
        self.ui_renderer.render_markdown("### Documents disponibles")
        
        for doc in documents:
            with self.ui_renderer.expander(f"📄 {doc.title}", expanded=False):
                self.ui_renderer.render_markdown(f"**ID**: {doc.id}")
                if doc.metadata:
                    self.ui_renderer.render_markdown("**Métadonnées**:")
                    for key, value in doc.metadata.items():
                        self.ui_renderer.render_markdown(f"- {key}: {value}")
                
                if self.ui_renderer.render_button("🗑️ Supprimer"):
                    if self.document_logic.delete_document(doc.id):
                        self.ui_renderer.render_success("Document supprimé")
                    else:
                        self.ui_renderer.render_error("Erreur lors de la suppression")
