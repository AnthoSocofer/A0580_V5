"""
Module de chargement de la configuration.

Ce module charge la configuration depuis:
1. Le fichier YAML par défaut
2. Les variables d'environnement
3. Un fichier de configuration personnalisé (optionnel)
"""

import os
from dataclasses import dataclass
from typing import Dict, Optional
from pathlib import Path
import yaml
import logging
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

@dataclass
class LoggingConfig:
    """Configuration du logging."""
    level: str
    format: str

@dataclass
class EmbeddingConfig:
    """Configuration du modèle d'embedding."""
    provider: str
    model: str

@dataclass
class RerankerConfig:
    """Configuration du modèle de reranking."""
    provider: str
    model: str

@dataclass
class SearchConfig:
    """Configuration de la recherche."""
    max_results: int
    min_score: float
    rerank_top_k: int

@dataclass
class KnowledgeBaseConfig:
    """Configuration des bases de connaissances."""
    storage_directory: str
    default_language: str
    max_results_per_search: int
    chunk_size: int
    min_length_for_chunking: int

@dataclass
class AppConfig:
    """Configuration principale de l'application."""
    version: str
    environment: str
    knowledge_base: KnowledgeBaseConfig
    logging: LoggingConfig
    embedding: EmbeddingConfig
    reranker: RerankerConfig
    search: SearchConfig

def _deep_update(base_dict: Dict, update_dict: Dict) -> None:
    """Met à jour récursivement un dictionnaire.
    
    Args:
        base_dict: Dictionnaire de base
        update_dict: Dictionnaire de mise à jour
    """
    for key, value in update_dict.items():
        if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
            _deep_update(base_dict[key], value)
        else:
            base_dict[key] = value

def _update_from_env(config_dict: Dict) -> None:
    """Met à jour la configuration depuis les variables d'environnement.
    
    Les variables d'environnement doivent être préfixées par APP_.
    Exemple: APP_KNOWLEDGE_BASE_STORAGE_DIR=/path/to/storage
    
    Args:
        config_dict: Dictionnaire de configuration à mettre à jour
    """
    env_prefix = "APP_"
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            # Conversion APP_KNOWLEDGE_BASE_STORAGE_DIR en ['knowledge_base', 'storage_dir']
            config_path = key[len(env_prefix):].lower().split('_')
            
            # Navigation dans le dictionnaire
            current_level = config_dict
            for part in config_path[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            
            # Conversion de type et assignation
            try:
                # Tentative de conversion en int
                current_level[config_path[-1]] = int(value)
            except ValueError:
                try:
                    # Tentative de conversion en float
                    current_level[config_path[-1]] = float(value)
                except ValueError:
                    # Sinon, garde la valeur comme string
                    current_level[config_path[-1]] = value

def _ensure_storage_directories(config_dict: Dict) -> None:
    """Crée les répertoires de stockage nécessaires.
    
    Args:
        config_dict: Dictionnaire de configuration contenant les chemins
    """
    logger = logging.getLogger(__name__)
    
    # Récupérer et créer le répertoire principal
    storage_dir = os.path.expanduser(config_dict["knowledge_base"]["storage_directory"])
    logger.info(f"Création des répertoires de stockage dans: {storage_dir}")
    
    # Créer les répertoires nécessaires
    os.makedirs(storage_dir, exist_ok=True)
    os.makedirs(os.path.join(storage_dir, "vector_storage"), exist_ok=True)
    os.makedirs(os.path.join(storage_dir, "metadata"), exist_ok=True)

def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Charge la configuration depuis les fichiers YAML et variables d'environnement.
    
    Args:
        config_path: Chemin vers un fichier de configuration personnalisé
        
    Returns:
        Configuration de l'application
    """
    # Chemin par défaut
    default_config_path = Path(__file__).parent / 'default.yml'
    
    if not default_config_path.exists():
        raise FileNotFoundError(
            f"Fichier de configuration par défaut non trouvé: {default_config_path}"
        )
    
    # Chargement config par défaut
    with open(default_config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    # Chargement config personnalisée
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            custom_config = yaml.safe_load(f)
            if custom_config:
                _deep_update(config_dict, custom_config)
    
    # Override par variables d'environnement
    _update_from_env(config_dict)
    
    # Créer les répertoires de stockage
    _ensure_storage_directories(config_dict)
    
    # Création des objets de configuration
    try:
        return AppConfig(
            version=config_dict.get("version", "1.0.0"),
            environment=config_dict.get("environment", "production"),
            knowledge_base=KnowledgeBaseConfig(
                storage_directory=os.path.expanduser(config_dict["knowledge_base"]["storage_directory"]),
                default_language=config_dict["knowledge_base"]["default_language"],
                max_results_per_search=config_dict["knowledge_base"]["max_results_per_search"],
                chunk_size=config_dict["knowledge_base"]["chunk_size"],
                min_length_for_chunking=config_dict["knowledge_base"]["min_length_for_chunking"]
            ),
            logging=LoggingConfig(
                level=config_dict["logging"]["level"],
                format=config_dict["logging"]["format"]
            ),
            embedding=EmbeddingConfig(
                provider=config_dict["embedding"]["provider"],
                model=config_dict["embedding"]["model"]
            ),
            reranker=RerankerConfig(
                provider=config_dict["reranker"]["provider"],
                model=config_dict["reranker"]["model"]
            ),
            search=SearchConfig(
                max_results=config_dict["search"]["max_results"],
                min_score=config_dict["search"]["min_score"],
                rerank_top_k=config_dict["search"]["rerank_top_k"]
            )
        )
    except KeyError as e:
        raise ValueError(f"Configuration invalide. Clé manquante: {str(e)}")
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement de la configuration: {str(e)}")

# Instance globale de configuration
config = load_config()