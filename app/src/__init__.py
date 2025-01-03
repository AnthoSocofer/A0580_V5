"""
Package principal de l'application.

Ce package contient tous les modules de l'application:
- config: Configuration de l'application
- core: Composants principaux
- modules: Modules fonctionnels
- pages: Pages de l'interface utilisateur
- utils: Utilitaires
"""

from src.config import config

__version__ = config.version
__all__ = ['__version__', 'config']
