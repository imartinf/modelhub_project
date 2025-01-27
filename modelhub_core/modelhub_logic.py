# modelhub_core/modelhub_logic.py
import os
import shutil
import subprocess
from .config import DB_PATH, SHARED_DIR
from .db_manager import DBManager

class ModelHubLogic:
    def __init__(self, db_path=DB_PATH, shared_dir=SHARED_DIR):
        self.db = DBManager(db_path)
        self.shared_dir = shared_dir
        # Asegúrate de inicializar la BD si no existe
        self.db.init_db()

    def clone_model(self, git_url):
        """Clona un repo Git en el directorio compartido y registra en BD."""
        # 1. Extraer nombre del repo
        name = os.path.splitext(os.path.basename(git_url))[0]

        # 2. Comprobar si existe ya
        if self.db.model_exists(name=name, url=git_url):
            return f"Error: El modelo '{name}' ({git_url}) ya está registrado."

        # 3. Determinar carpeta destino
        target_path = os.path.join(self.shared_dir, name)
        if os.path.exists(target_path):
            return f"Error: La carpeta de destino '{target_path}' ya existe."

        # 4. Clonar
        try:
            subprocess.check_output(["git", "clone", git_url, target_path])
        except subprocess.CalledProcessError as e:
            return f"Error al clonar {git_url}: {e}"

        # 5. Ajustar permisos
        self._protect_directory(target_path)

        # 6. Insertar en BD
        self.db.insert_model(name, source="git", url=git_url, path=target_path)
        return f"Modelo '{name}' clonado y protegido en '{target_path}'."

    def copy_local_model(self, local_path, model_name=None):
        """Copia un directorio local y lo registra en BD."""
        if not os.path.exists(local_path):
            return f"Error: La ruta local '{local_path}' no existe."
        if not os.path.isdir(local_path):
            return f"Error: '{local_path}' no es un directorio."

        if not model_name:
            model_name = os.path.basename(os.path.normpath(local_path))

        # Comprobar duplicados
        if self.db.model_exists(name=model_name, url=local_path):
            return f"Error: El modelo '{model_name}' (local:{local_path}) ya está registrado."

        target_path = os.path.join(self.shared_dir, model_name)
        if os.path.exists(target_path):
            return f"Error: La carpeta de destino '{target_path}' ya existe."

        try:
            shutil.copytree(local_path, target_path)
        except Exception as e:
            return f"Error copiando el modelo local: {e}"

        # Ajustar permisos
        self._protect_directory(target_path)

        # Insertar en BD
        self.db.insert_model(model_name, source="local", url=local_path, path=target_path)
        return f"Modelo '{model_name}' copiado y protegido en '{target_path}'."

    def list_models(self):
        """Lista modelos desde la BD."""
        rows = self.db.list_models()
        if not rows:
            return "No hay modelos disponibles"
        info = "Modelos disponibles:\n"
        for r in rows:
            name, source, url, path, created = r
            info += f" - {name} [{source}] -> {url}\n   Path: {path} (Creado: {created})\n"
        return info

    def _protect_directory(self, directory):
        """Cambia permisos de un directorio a solo lectura (ficheros -> 444, dirs -> 555)."""
        # Cambiar permisos del propio directorio raíz
        os.chmod(directory, 0o555)
        for root, dirs, files in os.walk(directory):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o555)
            for f in files:
                os.chmod(os.path.join(root, f), 0o444)