"""
Interface utilisateur pour la gestion des bases de connaissances.
"""
from typing import Optional
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
        self.ui_renderer.render_markdown("## 📚 Bases de connaissances")
        
        # Formulaire de création
        with self.ui_renderer.expander("➕ Créer une nouvelle base", expanded=False):
            self._render_create_form()
        
        # Liste des bases
        self._render_kb_list()
    
    def _render_create_form(self) -> None:
        """Affiche le formulaire de création."""
        title = self.ui_renderer.render_text_input(
            "Titre",
            placeholder="Titre de la base"
        )
        
        description = self.ui_renderer.render_text_area(
            "Description",
            placeholder="Description de la base"
        )
        
        if self.ui_renderer.render_button("Créer"):
            if title and description:
                kb_id = self.kb_logic.create_knowledge_base(title, description)
                if kb_id:
                    self.ui_renderer.render_success(
                        f"Base de connaissances créée avec succès (ID: {kb_id})"
                    )
                else:
                    self.ui_renderer.render_error(
                        "Erreur lors de la création de la base"
                    )
            else:
                self.ui_renderer.render_error(
                    "Le titre et la description sont requis"
                )
    
    def _render_kb_list(self) -> None:
        """Affiche la liste des bases de connaissances."""
        knowledge_bases = self.kb_logic.list_knowledge_bases()
        
        if not knowledge_bases:
            self.ui_renderer.render_info("Aucune base de connaissances disponible")
            return
        
        self.ui_renderer.render_markdown("### Bases disponibles")
        
        for kb in knowledge_bases:
            with self.ui_renderer.expander(f"📚 {kb.title}", expanded=False):
                self.ui_renderer.render_markdown(f"**ID**: {kb.id}")
                self.ui_renderer.render_markdown(f"**Description**: {kb.description}")
                
                # Formulaire de mise à jour
                new_title = self.ui_renderer.render_text_input(
                    "Nouveau titre",
                    value=kb.title
                )
                
                new_description = self.ui_renderer.render_text_area(
                    "Nouvelle description",
                    value=kb.description
                )
                
                col1, col2 = self.ui_renderer.columns(2)
                
                with col1:
                    if self.ui_renderer.render_button("💾 Mettre à jour"):
                        if new_title and new_description:
                            if self.kb_logic.update_knowledge_base(
                                kb.id, new_title, new_description
                            ):
                                self.ui_renderer.render_success("Base mise à jour")
                            else:
                                self.ui_renderer.render_error(
                                    "Erreur lors de la mise à jour"
                                )
                
                with col2:
                    if self.ui_renderer.render_button("🗑️ Supprimer"):
                        if self.kb_logic.delete_knowledge_base(kb.id):
                            self.ui_renderer.render_success("Base supprimée")
                        else:
                            self.ui_renderer.render_error(
                                "Erreur lors de la suppression"
                            )
