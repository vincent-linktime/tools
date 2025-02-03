import replicate
import requests
import time
import os

from typing import Dict, Any
from tools.common.logging import default_logger


class ReplicateClient:
    """
    Client for interacting with Replicate's API to perform various media processing tasks.
    """

    def __init__(self):
        self.logger = default_logger

    def image2text(self, image_path: str) -> str:
        """
        Generate a textual caption from the given image.

        Parameters:
            image_path (str): Path to the image file.

        Returns:
            str: Generated caption or an empty string if an error occurs.
        """
        try:
            with open(image_path, "rb") as image_file:
                payload = {"image": image_file}
                output = replicate.run(
                    "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
                    input=payload
                )
            if output.startswith("Caption:"):
                output = output.replace("Caption:", "").strip()
            return output
        except Exception as e:
            self.logger.error(
                f"Failed to generate text from image with path: {image_path}, error: {e}"
            )
            return ""

    def image2video(self, image_path: str, prompt: str, output_path: str) -> None:
        """
        Generate a video from the provided image and prompt.

        Parameters:
            image_path (str): Path to the input image.
            prompt (str): Prompt or caption to guide video generation.
            output_path (str): Path where the generated video will be saved.
        """
        try:
            with open(image_path, "rb") as image_file:
                self.logger.debug(f"Generating video from image: {image_path}")
                prediction = replicate.predictions.create(
                    model="kwaivgi/kling-v1.6-standard",
                    input={
                        "prompt": prompt,
                        "duration": 5,
                        "cfg_scale": 0.5,
                        "start_image": image_file,
                        "aspect_ratio": "9:16",
                        "negative_prompt": (
                            "distort the image, show anything that is not in the image, "
                            "like human hand or fingers."
                        )
                    }
                )

            timeout_seconds = 600
            while prediction.status not in {"succeeded", "failed", "canceled"} and timeout_seconds > 0:
                time.sleep(10)
                timeout_seconds -= 10
                prediction.reload()

            if prediction.status == "succeeded":
                video_url = prediction.output
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                response = requests.get(video_url)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                with open(output_path, "wb") as f:
                    f.write(response.content)
            else:
                self.logger.error(
                    f"Video generation did not succeed, status: {prediction.status}"
                )
        except Exception as e:
            self.logger.error(
                f"Failed to generate video from image with path: {image_path}, error: {e}"
            )

    def text2image(self, prompt: str, output_path: str) -> None:
        """
        Generate an image from text using the provided prompt.

        Parameters:
            prompt (str): Text prompt to generate the image.
            output_path (str): Path where the generated image will be saved.
        """
        try:
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "go_fast": True,
                    "num_outputs": 1,
                    "aspect_ratio": "16:9",
                    "output_format": "png",
                    "output_quality": 80,
                    "disable_safety_checker": False
                }
            )
            if not output:
                self.logger.error("No output received from text2image")
                return

            img_url = output[0]
            self.logger.debug(f"Image generated: {output}")
            response = requests.get(img_url)
            response.raise_for_status()
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            self.logger.error(
                f"Failed to generate image from text with prompt: {prompt}, error: {e}"
            )

    def speech2text(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe speech from an audio file.

        Parameters:
            audio_path (str): Path to the audio file.

        Returns:
            Dict[str, Any]: Transcription result from the API, or None if an error occurs.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                output = replicate.run(
                    "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
                    input={
                        "task": "transcribe",
                        "audio": audio_file,
                        "language": "None",
                        "timestamp": "chunk",
                        "diarise_audio": False
                    }
                )
            return output
        except Exception as e:
            self.logger.error(
                f"Failed to generate text from audio with path: {audio_path}, error: {e}"
            )
            return None
