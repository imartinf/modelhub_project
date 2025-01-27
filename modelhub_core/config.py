# modelhub_core/config.py
import os

# Rutas por defecto
DEFAULT_DB_PATH = "/var/modelhub/modelhub.db"
DEFAULT_SHARED_DIR = "/autofs/thau00a/shared_models"
PROJECT_PATH = "/home/root_gth/modelhub_project"

# O, si prefieres, se pueden leer variables de entorno:
DB_PATH = os.getenv("MODELHUB_DB_PATH", DEFAULT_DB_PATH)
SHARED_DIR = os.getenv("MODELHUB_SHARED_DIR", DEFAULT_SHARED_DIR)