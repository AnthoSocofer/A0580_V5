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
            placeholder: Texte à afficher quand aucune sélection
        """
        st.markdown(f"### {self.title}")
        
        # Mise à jour des options
        self.update_options(filter_state, items)
        
        # Affichage du sélecteur
        selected = st.multiselect(
            label=f"Sélectionner {self.title.lower()}",
            options=list(filter_state.options.keys()),
            format_func=lambda x: filter_state.options[x],
            key=f"{key_prefix}_{self.title.lower().replace(' ', '_')}",
            placeholder=placeholder or f"Choisir {self.title.lower()}..."
        )
        
        # Mise à jour de l'état et callback
        filter_state.selected_items = selected
        on_selection(selected)
