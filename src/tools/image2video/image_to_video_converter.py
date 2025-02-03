from tools.common.logging import default_logger
from tools.api.replicate.replicate_client import ReplicateClient

class ImageToVideoConverter:
    def __init__(self):
        self.logger = default_logger
        self.client = ReplicateClient()

    def convert(self, image_path: str, output_video_path: str) -> None:
        """
        Converts an image to a video by first extracting a caption (or prompt) from the image,
        then generating a video based on that caption.
        
        Parameters:
            image_path (str): Path to the input image file.
            output_video_path (str): Path where the generated video will be saved.
        """
        # Extract a caption or prompt from the image
        caption = self.client.image2text(image_path)
                
        # Generate the video using the image and the extracted caption
        self.client.image2video(image_path, caption, output_video_path)
