"""
Interface utilisateur pour la gestion des documents.
"""
import hashlib
from typing import Optional, BinaryIO
from src.ui.interfaces.ui_renderer import IUIRenderer
from src.ui.components.document.business.document_manager_logic import DocumentManagerLogic

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
            key=f"doc_uploader_{kb_id}",
            accept_multiple_files=False,
            help="Limite : 200MB",
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
    
    def _generate_button_key(self, kb_id: str, doc_id: str) -> str:
        """Génère une clé unique pour un bouton.
        
        Args:
            kb_id: ID de la base de connaissances
            doc_id: ID du document
            
        Returns:
            Clé unique pour le bouton
        """
        # Créer une chaîne unique à partir des IDs
        unique_string = f"{kb_id}_{doc_id}"
        # Générer un hash court mais unique
        return hashlib.md5(unique_string.encode()).hexdigest()[:8]
    
    def _render_document_list(self, kb_id: str) -> None:
        """Affiche la liste des documents."""
        documents = self.document_logic.list_documents(kb_id)
        
        if not documents:
            self.ui_renderer.render_info("Aucun document disponible")
            return
        
        self.ui_renderer.render_markdown("### Documents disponibles")
        
        for doc in documents:
            # Récupérer le titre du document depuis le dictionnaire
            doc_title = doc.get('title', doc.get('doc_id', 'Document sans titre'))
            doc_id = doc.get('doc_id', '')
            
            with self.ui_renderer.expander(f"📄 {doc_title}", expanded=False):
                self.ui_renderer.render_markdown(f"**ID**: {doc_id}")
                
                # Afficher les métadonnées si présentes
                metadata = doc.get('metadata', {})
                if metadata:
                    self.ui_renderer.render_markdown("**Métadonnées**:")
                    for key, value in metadata.items():
                        self.ui_renderer.render_markdown(f"- {key}: {value}")
                
                # Générer une clé unique pour le bouton
                button_key = self._generate_button_key(kb_id, doc_id)
                
                # Bouton de suppression avec clé unique
                if self.ui_renderer.render_button(
                    "🗑️ Supprimer",
                    key=f"delete_doc_button_{button_key}"
                ):
                    if self.document_logic.delete_document(doc_id):
                        self.ui_renderer.render_success("Document supprimé")
                    else:
                        self.ui_renderer.render_error(
                            "Erreur lors de la suppression"
                        )
