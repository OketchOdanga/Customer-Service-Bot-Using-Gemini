import gradio as gr
from db_utils import init_db
from core_logic import handle_user_request
# Initialize the database
init_db()

# Gradio interface
iface = gr.Interface(
    fn=handle_user_request,
    inputs=[
        gr.Textbox(label="Enter your complaint or request"),
        gr.Textbox(label="Enter your email address")
    ],
    outputs=gr.Markdown(label="Routing Result"),
    title="AI Customer Service Agent"
)


if __name__ == "__main__":
    iface.launch(share=True)

