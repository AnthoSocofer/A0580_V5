# Assistant Documentaire

Application de gestion et recherche documentaire basée sur l'IA.

## Fonctionnalités

- Gestion de bases de connaissances
- Upload et indexation de documents
- Recherche sémantique
- Interface de chat avec l'assistant
- Support multilingue

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

- `EMBEDDING_API_KEY` : Clé API OpenAI
- `RERANKER_API_KEY` : Clé API Cohere

## Utilisation

1. Lancer l'application :
```bash
cd app
streamlit run app.py
```

2. Ouvrir l'interface dans votre navigateur :
```
http://localhost:8501
```

## Structure du projet

```
app/
├── app.py              # Point d'entrée
├── data/              # Données
├── src/               # Code source
│   ├── config/        # Configuration
│   ├── core/          # Composants principaux
│   ├── modules/       # Modules fonctionnels
│   ├── pages/         # Interface utilisateur
│   └── utils/         # Utilitaires
└── tests/             # Tests
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

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
