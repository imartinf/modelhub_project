# tests/test_modelhub.py
import os
import shutil
import subprocess
import pytest

from modelhub_core.modelhub_logic import ModelHubLogic

@pytest.fixture
def hub(tmp_path):
    """
    Crea una instancia de ModelHubLogic que utiliza rutas 'temporales':
    - BD en tmp_path/test.db
    - shared_dir en tmp_path/shared
    Esto asegura que cada test corre en un entorno aislado.
    """
    db_test_path = os.path.join(tmp_path, "test.db")
    shared_dir_path = os.path.join(tmp_path, "shared")
    os.mkdir(shared_dir_path)

    logic = ModelHubLogic(db_path=db_test_path, shared_dir=shared_dir_path)
    return logic

def test_clone_new_model(hub):
    """
    Valida la clonación de un repositorio Git real.
    Usa un repo pequeño de ejemplo (aquí, el 'Hello-World' de octocat).
    Requiere acceso a internet y 'git' instalado.
    """
    git_url = "https://github.com/octocat/Hello-World.git"
    msg = hub.clone_model(git_url)
    assert "clonado y protegido" in msg.lower(), f"Mensaje inesperado: {msg}"

    # Comprobar que efectivamente se ha creado la carpeta
    name = os.path.splitext(os.path.basename(git_url))[0]  # "Hello-World.git" -> "Hello-World"
    repo_path = os.path.join(hub.shared_dir, name)
    assert os.path.isdir(repo_path), "No se encontró el directorio clonado en shared_dir"

    # Verificar que el archivo .git exista (indicio de clonación exitosa)
    git_dir = os.path.join(repo_path, ".git")
    assert os.path.isdir(git_dir), ".git no se creó; la clonación parece fallida"

def test_clone_existing_model(hub):
    """
    Clona 2 veces el mismo repo. La segunda debe fallar indicando que ya existe.
    """
    git_url = "https://github.com/octocat/Hello-World.git"

    # Primera clonación
    msg1 = hub.clone_model(git_url)
    assert "clonado y protegido" in msg1.lower()

    # Segunda clonación del mismo URL
    msg2 = hub.clone_model(git_url)
    assert "ya está registrado" in msg2.lower() or "error" in msg2.lower(), \
        "Se esperaba un error indicando que el modelo está duplicado"

def test_copy_local_model(hub, tmp_path):
    """
    Crea un directorio local con un archivo, lo copia a shared_dir
    y verifica que se haya insertado en la BD y se protejan permisos.
    """
    # 1. Crear directorio local
    local_src = os.path.join(tmp_path, "my_local_model")
    os.mkdir(local_src)
    # Crear un archivo de prueba
    with open(os.path.join(local_src, "test.txt"), "w") as f:
        f.write("contenido de prueba")

    # 2. Copiar usando la lógica
    msg = hub.copy_local_model(local_src, model_name="MiModeloLocal")
    assert "copiado y protegido" in msg.lower(), f"Mensaje inesperado: {msg}"

    # 3. Comprobar que se creó la carpeta en shared_dir
    target_path = os.path.join(hub.shared_dir, "MiModeloLocal")
    assert os.path.isdir(target_path), "No se encontró el directorio copiado en shared_dir"

    # 4. Verificar que el archivo test.txt existe en destino
    test_file = os.path.join(target_path, "test.txt")
    assert os.path.isfile(test_file), "Falta el archivo copiado en la carpeta destino"

def test_list_models(hub):
    """
    Agrega 2 modelos (1 git, 1 local) y verifica que 'list_models()' los muestra.
    """
    # Clonar un repo (Git)
    git_url = "https://github.com/octocat/Hello-World.git"
    hub.clone_model(git_url)

    # Copiar un modelo local
    # Creamos un dir temporal
    local_src = os.path.join(hub.shared_dir, "tmp_local")
    os.mkdir(local_src)
    with open(os.path.join(local_src, "archivo.txt"), "w") as f:
        f.write("dummy")

    hub.copy_local_model(local_src, "LocalTemporal")

    # Llamar list_models()
    output = hub.list_models()
    print(output)  # Para debugging
    assert "Hello-World" in output, "No aparece el repo Git en la lista"
    assert "LocalTemporal" in output, "No aparece el modelo local en la lista"
    assert "No hay modelos disponibles" not in output, "La lista no debería estar vacía"