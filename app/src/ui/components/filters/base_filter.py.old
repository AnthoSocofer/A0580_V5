"""
Composant de base pour les filtres.
"""
from typing import List, Dict, Any, Callable, Optional
import streamlit as st
from src.pages.states.filter_state import FilterState

class BaseFilter:
    """Composant de base pour le filtrage."""
    
    def __init__(self, title: str):
        """Initialise le composant de filtrage.
        
        Args:
            title: Titre du filtre à afficher
        """
        self.title = title
        
    def update_options(self, 
                      filter_state: FilterState,
                      items: List[Dict[str, Any]],
                      id_key: str = "id",
                      title_key: str = "title") -> None:
        """Met à jour les options du filtre.
        
        Args:
            filter_state: État du filtre
            items: Liste des éléments filtrables
            id_key: Clé pour l'identifiant dans les items
            title_key: Clé pour le titre dans les items
        """
        if not filter_state.initialized or len(filter_state.options) != len(items):
            filter_state.options = {
                str(item[id_key]): str(item[title_key]) 
                for item in items
            }
            # Sélectionner tous les éléments par défaut
            filter_state.selected_items = list(filter_state.options.keys())
            filter_state.initialized = True
    
    def render(self,
              filter_state: FilterState,
              items: List[Dict[str, Any]],
              on_selection: Callable[[List[str]], None],
              key_prefix: str = "",
              placeholder: Optional[str] = None) -> None:
        """Affiche le composant de filtrage.
        
        Args:
            filter_state: État du filtre
            items: Liste des éléments filtrables
            on_selection: Callback appelé lors d'une sélection
            key_prefix: Préfixe pour les clés Streamlit
            placeholder: Texte de placeholder pour le sélecteur
        """
        # Mettre à jour les options si nécessaire
        self.update_options(filter_state, items)
        
        # Afficher le sélecteur multiple
        selected_titles = st.multiselect(
            self.title,
            options=list(filter_state.options.values()),
            default=[filter_state.options[item_id] for item_id in filter_state.selected_items],
            key=f"{key_prefix}filter_{self.title}",
            placeholder=placeholder or f"Sélectionner des {self.title.lower()}..."
        )
        
        # Mettre à jour la sélection
        selected_ids = [
            item_id
            for item_id, title in filter_state.options.items()
            if title in selected_titles
        ]
        
        # Si la sélection a changé, mettre à jour l'état et appeler le callback
        if selected_ids != filter_state.selected_items:
            filter_state.selected_items = selected_ids
            on_selection(selected_ids)
