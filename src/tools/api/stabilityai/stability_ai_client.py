import os
import click
import requests
import time

from tools.common.logging import default_logger


class StabilityAIClient:
    """
    Client for interacting with the Stability AI Image-to-Video API.
    """

    def __init__(self):
        self.logger = default_logger
        self.api_key = os.getenv("STABILITY_AI_API_KEY")
        if not self.api_key:
            self.logger.error("STABILITY_AI_API_KEY environment variable not set.")

    def _write_video_file(self, content: bytes, output_path: str) -> None:
        """Ensure output directory exists and write video content to file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as video_file:
            video_file.write(content)
        self.logger.debug(f"Video written to {output_path}")

    def _get_video(self, generation_id: str, output_path: str) -> requests.Response:
        """
        Retrieve the generated video using the generation ID.
        If successful, write the video content to the specified output path.
        """
        url = f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}"
        try:
            response = requests.get(
                url,
                headers={
                    "accept": "video/*",  # For raw video; change to application/json if expecting JSON.
                    "authorization": self.api_key,
                },
            )
            if response.status_code != 200:
                self.logger.error(
                    f"Failed to get video for ID: {generation_id}, response: {response.json()}"
                )
                return None

            self._write_video_file(response.content, output_path)
            return response

        except Exception as e:
            self.logger.error(f"Failed to get video for ID: {generation_id}, error: {e}")
            return None

    def _get_generation_status(self, generation_id: str) -> requests.Response:
        """
        Retrieve the current status of the video generation.
        """
        url = f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}"
        try:
            response = requests.get(
                url,
                headers={
                    "accept": "video/*",  # Or application/json if expecting status info in JSON.
                    "authorization": self.api_key,
                },
            )
            return response
        except Exception as e:
            self.logger.error(f"Failed to get generation status for ID: {generation_id}, error: {e}")
            return None

    def image2video(self, image_path: str, prompt: str, output_path: str) -> None:
        """
        Convert an image to a video by sending a request to the Stability AI API.
        The prompt is provided to guide video generation.
        """
        post_url = "https://api.stability.ai/v2beta/image-to-video"
        try:
            # Use a context manager to ensure the file is properly closed
            with open(image_path, "rb") as image_file:
                response = requests.post(
                    post_url,
                    headers={
                        "authorization": self.api_key
                    },
                    files={
                        "image": image_file
                    },
                    data={
                        "seed": 0,
                        "cfg_scale": 1.8,
                        "motion_bucket_id": 127,
                        "prompt": prompt  # Assuming the API accepts a prompt; adjust if needed.
                    },
                )
            
            if response.status_code != 200:
                self.logger.error(
                    f"Failed to create video generation request for image: {image_path}, response: {response.json()}"
                )
                return

            try:
                response_json = response.json()
                generation_id = response_json.get("id")
                self.logger.debug(f"Video generation ID: {generation_id}")
                if not generation_id:
                    self.logger.error(f"Generation ID not found in response: {response_json}")
                    return
            except Exception as e:
                self.logger.error(f"Failed to extract generation ID from response: {response.json()}, error: {e}")
                return

            # Poll for video generation status
            timeout = 600
            wait_interval = 15
            status_response = self._get_generation_status(generation_id)
            while status_response and status_response.status_code != 200 and timeout > 0:
                self.logger.debug(f"Waiting for video generation: {status_response.json()}")
                time.sleep(wait_interval)
                timeout -= wait_interval
                status_response = self._get_generation_status(generation_id)

            if status_response and status_response.status_code == 200:
                self._write_video_file(status_response.content, output_path)
                self.logger.debug(f"Video generated successfully from image: {image_path}")
            else:
                error_details = status_response.json() if status_response else "No response"
                self.logger.error(
                    f"Failed to retrieve video for image: {image_path}, response: {error_details}"
                )

        except Exception as e:
            self.logger.error(f"Failed to generate video from image {image_path}, error: {e}")


@click.command()
@click.option("--generation_id", "-g", required=True, type=str, help="Video generation ID.")
@click.option("--video_path", "-v", required=True, type=str, help="Path to the output video file.")
def get_video(generation_id: str, video_path: str):
    """
    Command-line interface to retrieve a generated video using its generation ID.
    """
    default_logger.setLevel("DEBUG")
    stabilityai_client = StabilityAIClient()
    stabilityai_client._get_video(generation_id, video_path)


if __name__ == "__main__":
    get_video()
