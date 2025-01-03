"""
Package pages contenant les interfaces utilisateur de l'application.

Modules:
- components: Composants réutilisables de l'interface
- sidebar_page: Page de gestion des bases de connaissances
- chat_page: Page de chat avec l'assistant
"""

from src.pages.sidebar_page import KnowledgeBasePage
from src.pages.chat_page import ChatPage
from src.pages.components import *

__all__ = [
    'KnowledgeBasePage',
    'ChatPage',
]
