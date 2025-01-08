# Assistant Documentaire

Application de gestion et recherche documentaire basée sur l'IA.

## Fonctionnalités

- Gestion de bases de connaissances avec stockage vectoriel (ChromaDB)
- Upload et indexation de documents avec chunking intelligent
- Recherche sémantique avec réordonnancement des résultats
- Interface de chat avec assistant IA
- Support multilingue (Français, Anglais)
- Filtrage par base de connaissances et documents
- Gestion des modèles LLM (OpenAI, etc.)

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-compte/assistant-documentaire.git
cd assistant-documentaire
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

## Configuration

La configuration de l'application se fait via :
- Fichier YAML (`app/src/config/default.yml`)
- Variables d'environnement (préfixe `APP_`)
- Fichier `.env` pour les clés API

### Variables d'environnement requises :

- `OPENAI_API_KEY` : Clé API OpenAI pour les embeddings et LLM
- `COHERE_API_KEY` : Clé API Cohere pour le reranking

## Architecture

L'application suit une architecture en couches avec séparation des responsabilités :

### Core (Noyau)
- Gestion des bases de connaissances
- Moteur de recherche vectorielle
- Gestion de l'état de l'application
- Types et interfaces communs

### UI (Interface Utilisateur)
Composants modulaires suivant une architecture en 3 couches :
- `business/` : Logique métier et règles de gestion
- `data/` : Accès et manipulation des données
- `view/` : Interface utilisateur et rendu Streamlit

### Composants principaux
- `chat/` : Interface conversationnelle avec l'assistant
- `search/` : Recherche sémantique et filtrage
- `document/` : Gestion des documents et métadonnées
- `knowledge_base/` : Gestion des bases de connaissances
- `language_model/` : Intégration des modèles de langage

### Interfaces
- Contrats entre les composants
- Abstraction des dépendances externes
- États et types partagés

### External
Intégration avec les services externes :
- Modèles d'embeddings (OpenAI)
- Reranking (Cohere)
- Stockage vectoriel (ChromaDB)

## Structure du projet

```
app/
├── main.py            # Point d'entrée de l'application
├── data/              # Données et stockage
├── src/               # Code source
│   ├── config/        # Configuration
│   │   └── default.yml
│   ├── core/          # Composants principaux
│   │   ├── knowledge_base_manager.py
│   │   ├── search_engine.py
│   │   ├── state_manager.py
│   │   └── types.py
│   ├── ui/            # Interface utilisateur
│   │   ├── components/    # Composants réutilisables
│   │   │   ├── chat/         # Composant de chat
│   │   │   │   ├── business/     # Logique métier
│   │   │   │   ├── data/         # Gestion des données
│   │   │   │   └── view/         # Interface utilisateur
│   │   │   ├── search/       # Composant de recherche
│   │   │   ├── document/     # Gestion des documents
│   │   │   ├── knowledge_base/  # Gestion des bases de connaissances
│   │   │   └── language_model/  # Gestion des modèles de langage
│   │   ├── interfaces/    # Interfaces des composants
│   │   └── states/        # États de l'application
│   └── external/       # Modules externes
└── tests/             # Tests unitaires et d'intégration
```

## Développement

1. Installation des dépendances de développement :
```bash
pip install -r requirements-dev.txt
```

2. Lancer les tests :
```bash
pytest
```

3. Conventions de code :
- Type hints pour toutes les fonctions
- Docstrings pour les classes et méthodes
- Tests unitaires pour la logique métier
- Architecture hexagonale avec interfaces claires

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
