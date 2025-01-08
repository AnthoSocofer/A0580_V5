"""
Configuration des tests.
"""
import os
import sys

# Ajout du répertoire racine au PYTHONPATH
app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if app_root not in sys.path:
    sys.path.insert(0, app_root)
