# modelhub_app/main_app.py
import gradio as gr
from modelhub_core.modelhub_logic import ModelHubLogic

# Crear instancia con valores por defecto
hub = ModelHubLogic()

def ui_clone_model(git_url):
    return hub.clone_model(git_url)

def ui_copy_local_model(local_path, model_name):
    return hub.copy_local_model(local_path, model_name)

def ui_list_models():
    return hub.list_models()

with gr.Blocks() as demo:
    gr.Markdown("# Model Hub")
    
    with gr.Tab("Clonar desde Git"):
        git_url_input = gr.Textbox(label="URL de repositorio Git")
        clone_button = gr.Button("Descargar modelo")
        clone_output = gr.Textbox(label="Resultado", lines=3)

        clone_button.click(ui_clone_model, inputs=[git_url_input], outputs=[clone_output])

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
        list_button.click(ui_list_models, outputs=[list_output])

demo.launch(share=True, server_name="0.0.0.0", server_port=7860)