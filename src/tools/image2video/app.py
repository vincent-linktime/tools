from datetime import date

import gradio as gr
from tools.image2video.image2video_converter import Image2VideoConverter
from tools.image2video.image2video_models import Image2VideoModelType

def convert_image_to_video(image_path: str, prompt: str, model_type: str):
    """
    Generator function that converts an image to a video using the provided prompt and model type.
    
    Yields:
      - A "Processing..." status message and no video immediately.
      - After conversion, an empty status message and the path to the generated video.
    
    Parameters:
      image_path (str): The file path of the uploaded image.
      prompt (str): The text prompt for video conversion.
      model_type (str): The selected image2video model type.
    """
    # Immediately update the status to "Processing..."
    yield "Processing...", None

    try:
        # Create an instance of ImageToVideoConverter
        image2video_converter = Image2VideoConverter()
        
        # Define an output path for the generated video.
        time_str = date.today().strftime("%Y-%m-%d-%H-%M-%S")
        output_video_path = f"output/video-{time_str}.mp4"
        
        # Run the conversion using the provided prompt and model type.
        # (Ensure that ImageToVideoConverter.convert is updated to accept model_type if needed.)
        image2video_converter.convert(image_path, prompt, output_video_path, model_type)
        
        # Once complete, yield an empty status and the video file path.
        yield "", output_video_path
    except Exception as error:
        # If an error occurs, yield the error message and no video.
        yield f"Error during conversion: {error}", None

# Build the Gradio interface using Blocks with the Origin theme (light theme)
with gr.Blocks(theme=gr.themes.Origin()) as demo:
    # Row 1: Image upload (reduced size)
    with gr.Row():
        uploaded_image = gr.Image(
            label="Upload Image (PNG/JPG)", 
            type="filepath", 
            height=512, 
            width=512
        )
    
    # Row 2: Prompt input
    with gr.Row():
        prompt_input = gr.Textbox(
            label="Prompt", 
            value="", 
            placeholder="Enter a prompt or leave blank to auto-generate"
        )
    
    # Row 3: Model selection dropdown and Run button
    with gr.Row():
        model_type_dropdown = gr.Dropdown(
            label="Select Model Type",
            choices=[member.value for member in Image2VideoModelType],
            value=Image2VideoModelType.REPLICATE.value
        )
        run_conversion_button = gr.Button("Run")
    
    # Row 4: Status message and video output (reduced video size)
    with gr.Row():
        with gr.Column():
            status_message = gr.Markdown(value="")
            video_player = gr.Video(
                label="Output Video", 
                height=512, 
                width=512
            )
    
    # Wire the run button to the convert_image_to_video generator function.
    run_conversion_button.click(
        fn=convert_image_to_video,
        inputs=[uploaded_image, prompt_input, model_type_dropdown],
        outputs=[status_message, video_player],
        show_progress=True
    )

# Launch the Gradio app
demo.launch()
