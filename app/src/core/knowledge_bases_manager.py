"""
Gestionnaire de bases de connaissances utilisant ChromaDB.
"""

import os
import json
import logging
import chromadb
from typing import Dict, List, Optional, Any
import shutil
from dsrag.knowledge_base import KnowledgeBase
from dsrag.database.vector.types import MetadataFilter
from src.config import config
from dsrag.embedding import OpenAIEmbedding
from dsrag.reranker import CohereReranker
from pathlib import Path

class KnowledgeBasesManager:
    """Gestionnaire de bases de connaissances."""
    
    def __init__(self, storage_directory: Optional[str] = None):
        """Initialise le gestionnaire de bases de connaissances."""
        self.storage_directory = os.path.expanduser(
            storage_directory if storage_directory else config.knowledge_base.storage_directory
        )
        self.vector_storage_path = os.path.join(self.storage_directory, "vector_storage")
        self.metadata_dir = os.path.join(self.storage_directory, "metadata")
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        # Client ChromaDB pour la gestion des collections
        self.chroma_client = chromadb.PersistentClient(path=self.vector_storage_path)
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Cache des bases de connaissances
        self._knowledge_bases: Dict[str, KnowledgeBase] = {}
        self._loading = False  # Flag pour éviter les chargements récursifs
        self._load_existing_bases()
    
    def _load_existing_bases(self) -> None:
        """Charge les bases de connaissances existantes depuis le stockage."""
        if self._loading:  # Évite les chargements récursifs
            return
            
        try:
            self._loading = True
            if not os.path.exists(self.metadata_dir):
                self.logger.warning(f"Le répertoire de métadonnées n'existe pas: {self.metadata_dir}")
                return
                
            for filename in os.listdir(self.metadata_dir):
                if filename.endswith('.json'):
                    kb_id = filename[:-5]
                    if kb_id not in self._knowledge_bases:  # Évite les rechargements inutiles
                        try:
                            kb = KnowledgeBase(
                                kb_id=kb_id,
                                storage_directory=self.storage_directory,
                                exists_ok=True
                            )
                            self._knowledge_bases[kb_id] = kb
                            self.logger.info(f"Base de connaissances chargée: {kb_id}")
                        except Exception as e:
                            self.logger.warning(f"Erreur lors du chargement de la base {kb_id}: {str(e)}")
        finally:
            self._loading = False

    def _get_document_count(self, kb: KnowledgeBase) -> int:
        """Retourne le nombre de documents dans une base."""
        try:
            # Utilise l'API de dsrag pour obtenir les IDs des documents
            doc_ids = kb.chunk_db.get_all_doc_ids()
            return len(doc_ids)
        except Exception as e:
            self.logger.warning(f"Erreur lors du comptage des documents: {str(e)}")
            return 0

    def get_knowledge_base(self, kb_id: str) -> Optional[KnowledgeBase]:
        """Récupère une base de connaissances par son ID."""
        if kb_id in self._knowledge_bases:
            return self._knowledge_bases[kb_id]
            
        metadata_file = os.path.join(self.metadata_dir, f"{kb_id}.json")
        if not os.path.exists(metadata_file):
            self.logger.warning(f"La base {kb_id} n'existe pas")
            return None
            
        try:
            kb = KnowledgeBase(
                kb_id=kb_id,
                storage_directory=self.storage_directory,
                exists_ok=True
            )
            self._knowledge_bases[kb_id] = kb
            return kb
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la base {kb_id}: {str(e)}")
            return None

    def list_knowledge_bases(self) -> List[Dict[str, Any]]:
        """Liste toutes les bases de connaissances disponibles."""
        kb_list = []
        for filename in os.listdir(self.metadata_dir):
            if filename.endswith('.json'):
                kb_id = filename[:-5]
                try:
                    kb = self.get_knowledge_base(kb_id)
                    if kb:
                        kb_info = {
                            'kb_id': kb_id,
                            'title': kb.kb_metadata.get('title', kb_id),
                            'description': kb.kb_metadata.get('description', ''),
                            'language': kb.kb_metadata.get('language', config.knowledge_base.default_language),
                            'document_count': self._get_document_count(kb)
                        }
                        # Ajouter la liste des documents
                        kb_info['documents'] = self.list_documents(kb_id)
                        kb_list.append(kb_info)
                except Exception as e:
                    self.logger.warning(f"Erreur lors de la lecture des métadonnées de {kb_id}: {str(e)}")
                    kb_list.append({
                        'kb_id': kb_id,
                        'title': kb_id,
                        'description': str(e),
                        'language': config.knowledge_base.default_language,
                        'document_count': 0,
                        'documents': []
                    })
        return kb_list

    def create_knowledge_base(
        self,
        kb_id: str,
        title: str = "",
        description: str = "",
        language: str = "fr",
        embedding_provider: str = "openai",
        embedding_model: str = "text-embedding-3-small",
        embedding_dimension: Optional[int] = None,
        reranker_provider: str = "cohere",
        reranker_model: str = "rerank-multilingual-v3.0",
        exists_ok: bool = False,
        **kwargs
    ) -> KnowledgeBase:
        """Crée une nouvelle base de connaissances avec configuration personnalisée
        
        Args:
            kb_id: Identifiant unique de la base
            title: Titre de la base
            description: Description de la base
            language: Langue des documents ("fr", "en", etc.)
            embedding_provider: Fournisseur du modèle d'embedding
            embedding_model: Nom du modèle d'embedding
            embedding_dimension: Dimension des vecteurs (optionnel)
            reranker_provider: Fournisseur du modèle de reranking
            reranker_model: Nom du modèle de reranking
            exists_ok: Si True, écrase la base si elle existe déjà
            
        Returns:
            La base de connaissances créée
        """
        try:
            self.logger.info(f"Création de la base {kb_id} dans {self.storage_directory}")
            
            # Vérifier que les répertoires existent
            os.makedirs(self.storage_directory, exist_ok=True)
            os.makedirs(self.metadata_dir, exist_ok=True)
            
            # Vérifier si la base existe déjà
            if kb_id in self._knowledge_bases:
                if not exists_ok:
                    raise ValueError(f"La base {kb_id} existe déjà")
                self.delete_knowledge_base(kb_id)
            
            # Créer les modèles
            embedding_model = self._create_embedding_model(
                embedding_provider,
                embedding_model,
                embedding_dimension
            )
            
            reranker = self._create_reranker(
                reranker_provider,
                reranker_model
            )
            
            # Créer la base de connaissances
            kb = KnowledgeBase(
                kb_id=kb_id,
                storage_directory=self.storage_directory,
                embedding_model=embedding_model,
                reranker=reranker,
                exists_ok=exists_ok,
                title=title,
                description=description,
                language=language,
                **kwargs
            )
            
            # La base est automatiquement sauvegardée par KnowledgeBase.__init__
            
            # Mettre à jour le cache
            self._knowledge_bases[kb_id] = kb
            
            self.logger.info(f"Base de connaissances créée avec succès: {kb_id}")
            return kb
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de la base {kb_id}: {str(e)}")
            raise

    def _create_embedding_model(
        self,
        provider: str = "openai",
        model_name: str = "text-embedding-3-small",
        dimension: Optional[int] = None
    ) -> OpenAIEmbedding:
        """Crée une instance du modèle d'embedding selon la configuration"""
        if provider == "openai":
            return OpenAIEmbedding(model=model_name, dimension=dimension)
        raise ValueError(f"Provider d'embedding non supporté: {provider}")

    def _create_reranker(
        self,
        provider: str = "cohere",
        model_name: str = "rerank-multilingual-v3.0"
    ) -> CohereReranker:
        """Crée une instance du modèle de reranking selon la configuration"""
        if provider == "cohere":
            return CohereReranker(model=model_name)
        raise ValueError(f"Provider de reranking non supporté: {provider}")

    def delete_knowledge_base(self, kb_id: str) -> bool:
        """Supprime une base de connaissances."""
        try:
            # Si la base est dans le cache, utiliser son API pour la suppression
            if kb_id in self._knowledge_bases:
                kb = self._knowledge_bases[kb_id]
                kb.delete()
                del self._knowledge_bases[kb_id]
            else:
                # Si la base n'est pas dans le cache (erreur de chargement), supprimer manuellement
                # Supprimer le fichier de métadonnées
                metadata_path = os.path.join(self.metadata_dir, f"{kb_id}.json")
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)
                
                # Supprimer le répertoire de la base
                kb_path = os.path.join(self.storage_directory, kb_id)
                if os.path.exists(kb_path):
                    shutil.rmtree(kb_path)
                
                # Supprimer la collection ChromaDB
                try:
                    self.chroma_client.delete_collection(kb_id)
                except Exception:
                    pass
            
            self.logger.info(f"Base de connaissances supprimée: {kb_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression de la base {kb_id}: {str(e)}")
            return False

    def list_documents(self, kb_id: str) -> List[Dict[str, Any]]:
        """Liste tous les documents d'une base de connaissances."""
        kb = self.get_knowledge_base(kb_id)
        if not kb:
            return []
            
        documents = []
        try:
            doc_ids = kb.chunk_db.get_all_doc_ids()
            for doc_id in doc_ids:
                try:
                    doc = kb.chunk_db.get_document(doc_id, include_content=False)
                    if doc:
                        documents.append({
                            'doc_id': doc_id,
                            'title': doc.get('title', doc_id)
                        })
                except Exception as e:
                    self.logger.warning(f"Erreur lors de la récupération du document {doc_id}: {str(e)}")
                    continue
        except Exception as e:
            self.logger.error(f"Erreur lors de la liste des documents: {str(e)}")
            
        return documents
    
    # Alias pour compatibilité
    get_documents = list_documents

    def delete_document(self, kb_id: str, doc_id: str) -> bool:
        """Supprime un document d'une base de connaissances.
        
        Args:
            kb_id: ID de la base de connaissances
            doc_id: ID du document à supprimer
            
        Returns:
            bool: True si le document a été supprimé avec succès
        """
        try:
            kb = self.get_knowledge_base(kb_id)
            if not kb:
                raise ValueError(f"Base de connaissances {kb_id} introuvable")
            
            # Supprimer le document de la base
            kb.delete_document(doc_id)
            self.logger.info(f"Document {doc_id} supprimé de la base {kb_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du document {doc_id} de la base {kb_id}: {str(e)}")
            return False

    def add_document(
        self,
        kb_id: str,
        doc_id: str,
        file_path: str,
        document_title: str,
        auto_context_config: Dict[str, Any]
    ) -> bool:
        """Ajoute un document à une base de connaissances.
        
        Args:
            kb_id: ID de la base de connaissances
            doc_id: ID unique du document
            file_path: Chemin vers le fichier à ajouter
            document_title: Titre du document
            auto_context_config: Configuration pour le chunking automatique
            
        Returns:
            bool: True si le document a été ajouté avec succès
        """
        try:
            kb = self.get_knowledge_base(kb_id)
            if not kb:
                raise ValueError(f"Base de connaissances {kb_id} introuvable")
            
            # Ajouter le document à la base
            kb.add_document(
                doc_id=doc_id,
                file_path=file_path,
                document_title=document_title,
                auto_context_config=auto_context_config
            )
            self.logger.info(f"Document {doc_id} ajouté à la base {kb_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout du document {doc_id} à la base {kb_id}: {str(e)}")
            return False