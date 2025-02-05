from tools.common.logging import default_logger
from tools.api.replicate.replicate_client import ReplicateClient
from tools.api.stabilityai.stability_ai_client import StabilityAIClient
from tools.image2video.image2video_models import Image2VideoModelType

class Image2VideoConverter:
    def __init__(self):
        self.logger = default_logger
        self.replicate_client = ReplicateClient()
        self.stabilityai_client = StabilityAIClient()

    def convert(self, image_path: str, prompt: str, output_video_path: str, model: str) -> None:
        """
        Converts an image to a video by first extracting a caption (or prompt) from the image,
        then generating a video based on that caption.
        
        Parameters:
            image_path (str): Path to the input image file.
            output_video_path (str): Path where the generated video will be saved.
        """
        # Generate the video using the image and the extracted caption
        if model is None:
            self.logger.error("Image2Video Model is not specified")
            return
        
        if model == Image2VideoModelType.REPLICATE.value:
            self.logger.debug(f"Generating video using Replicate model")
            self.replicate_client.image2video(image_path, prompt, output_video_path)
        elif model == Image2VideoModelType.STABILITY.value:
            self.logger.debug(f"Generating video using StabilityAI model")
            self.stabilityai_client.image2video(image_path, output_video_path)
        else:
            self.logger.error(f"Unsupported model: {model}")
            return
