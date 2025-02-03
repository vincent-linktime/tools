import gradio as gr
from tools.image2video.image_to_video_converter import ImageToVideoConverter

def convert_image_to_video(image_path: str):
    """
    Generator function that converts an image to a video.
    
    Yields:
      - A "Processing..." status message and no video immediately.
      - After conversion, an empty status message and the path to the generated video.
    
    Parameters:
      image_path (str): The file path of the uploaded image.
    """
    # Immediately update the status to "Processing..."
    yield "Processing...", None

    try:
        # Create an instance of ImageToVideoConverter
        image_to_video_converter = ImageToVideoConverter()
        
        # Define an output path for the generated video.
        output_video_path = "output/video.mp4"
        
        # Run the conversion (this may take a while depending on your API call)
        image_to_video_converter.convert(image_path, output_video_path)
        
        # Once complete, yield an empty status and the video file path
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
    
    # Row 2: Run button
    with gr.Row():
        run_conversion_button = gr.Button("Run")
    
    # Row 3: Status message and video output (reduced video size)
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
        inputs=[uploaded_image],
        outputs=[status_message, video_player],
        show_progress=True
    )

# Launch the Gradio app
demo.launch()
