import http.client
import json
import os
import requests

import time
from typing import Dict, Any

from tools.common.logging import default_logger

class PiAPIClient:
    def __init__(self):
        self.logger = default_logger
        self.api_key = os.getenv("PI_API_KEY")
        self.conn = http.client.HTTPSConnection("api.piapi.ai")

    def _get_task(self, task_id: str) -> Dict[str, Any]:
        try:
            headers = {"x-api-key": self.api_key}
            self.conn.request("GET", f"/api/v1/task/{task_id}", headers=headers)
            res = self.conn.getresponse()
            data = res.read()
            return json.loads(data.decode("utf-8"))
        except Exception as e:
            self.logger.error(f"Failed to get task with task_id: {task_id}, error: {e}")

    def _get_video(self, task: Dict[str, Any], output_path: str) -> None:
        try:
            video_url = task["data"]["output"]["works"][0]["video"][
                "resource_without_watermark"
            ]
            self.logger.debug(
                f"Video generated successfully, downloading video from url: {video_url}"
            )
            response = requests.get(video_url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)               
            self.logger.debug(f"Video downloaded successfully to path: {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to download video, error: {e}")

    def image2video(self, image_url: str, prompt: str, output_path: str) -> None:
        try:
            self.logger.debug(f"Generating video from image with url: {image_url}")
            payload = json.dumps(
                {
                    "model": "kling",
                    "task_type": "video_generation",
                    "input": {
                        "image_url": image_url,
                        "prompt": prompt,
                        "negative_prompt": "distort the image, show anything that is not in the image, like human hand or fingers.",
                        "cfg_scale": 0.5,
                        "duration": 5,
                        "aspect_ratio": "9:16",
                        "camera_control": {
                            "type": "simple",
                            "config": {
                                "horizontal": 0,
                                "vertical": 0,
                                "pan": -10,
                                "tilt": 0,
                                "roll": 0,
                                "zoom": 0,
                            },
                        },
                        "mode": "std",
                    },
                    "config": {
                        "service_mode": "",
                        "webhook_config": {"endpoint": "", "secret": ""},
                    },
                }
            )

            headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

            self.conn.request("POST", "/api/v1/task", payload, headers)
            res = self.conn.getresponse()
            data = res.read().decode("utf-8")
            self.logger.debug(f"Video task submitted: {data}")
            task_id = json.loads(data)["task_id"]

            timeout = 600
            task = self._get_task(task_id)
            self.logger.debug(f"Video task retrieved: \n{json.dumps(task, indent=4)}")
            while timeout > 0 and (
                task["data"]["status"] != "Completed"
                or task["data"]["status"] != "Failed"
            ):
                time.sleep(15)
                timeout -= 15
                task = self._get_task(task_id)

            if task["data"]["status"] == "Completed":
                self._get_video(task, output_path)
            else:
                self.logger.error(
                    f"Failed to generate video from image with url: {image_url},"
                    f" task status: {task['data']['status']}"
                )
        except Exception as e:
            self.logger.error(
                f"Failed to generate video from image with path: {image_url}, error: {e}"
            )
