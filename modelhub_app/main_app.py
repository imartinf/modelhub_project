# modelhub_app/main_app.py
import gradio as gr
from modelhub_core.modelhub_logic import ModelHubLogic
import os

# Crear instancia con valores por defecto
hub = ModelHubLogic()

def ui_clone_model(git_url, model_name):
    return hub.clone_model(git_url, name=model_name)

def ui_copy_local_model(local_path, model_name):
    return hub.copy_local_model(local_path, model_name)

def ui_list_models():
    changes = hub.refresh_db()
    models_list = hub.list_models()
    return changes, models_list

with gr.Blocks() as demo:
    gr.Markdown("# Model Hub")
    
    with gr.Tab("Clonar desde Git"):
        git_url_input = gr.Textbox(label="URL de repositorio Git", value="https://hub/repo.git")
        git_name_input = gr.Textbox(label="Nombre del modelo (opcional)")
        
        def update_model_name(git_url):
            return os.path.basename(git_url).replace(".git", "")
        
        git_url_input.change(fn=update_model_name, inputs=[git_url_input], outputs=[git_name_input])
        clone_button = gr.Button("Descargar modelo")
        clone_output = gr.Textbox(label="Resultado", lines=3)

        clone_button.click(ui_clone_model, inputs=[git_url_input, git_name_input], outputs=[clone_output])

    with gr.Tab("Copiar modelo local"):
        local_path_input = gr.Textbox(label="Ruta local del modelo (directorio)")
        local_name_input = gr.Textbox(label="Nombre del modelo (opcional)")
        copy_button = gr.Button("Copiar modelo local")
        copy_output = gr.Textbox(label="Resultado", lines=3)

        copy_button.click(ui_copy_local_model,
                          inputs=[local_path_input, local_name_input],
                          outputs=[copy_output])

    with gr.Tab("Listar modelos"):
        list_button = gr.Button("Refrescar lista")
        list_output = gr.Textbox(label="Modelos", lines=10)
        refresh_info = gr.Textbox(label="Cambios", lines=3)

        list_button.click(ui_list_models, outputs=[refresh_info, list_output])

demo.launch(share=False, server_name="0.0.0.0", server_port=7860)