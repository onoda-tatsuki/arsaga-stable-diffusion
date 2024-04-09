from __future__ import annotations

from typing import Optional

import requests
from requests.exceptions import RequestException

from arsaga_stable_diffusion.schemas.types import image_aspect, image_format
from arsaga_stable_diffusion.stable_diffusion.base import (
    BaseImageGenerator,
    ImageGeneratorFactory,
)


@ImageGeneratorFactory.register("v2")
class V2ImageGenerator(BaseImageGenerator):
    def __init__(self):
        super().__init__()

    def generate_image(
        self,
        prompt: str,
        aspect_ratio: image_aspect = "1:1",
        image_format: image_format = "webp",
        art_style: Optional[str] = None,
        negative_prompt: Optional[str] = None,
    ) -> bytes:
        if self.api_key is None:
            raise ValueError("Missing Stability AI API Key")

        if art_style:
            request_prompt = (
                f"({self.quality_prompt}:1.3), " + f"({art_style}:1.4), " + prompt
            )
        else:
            request_prompt = f"({self.quality_prompt}:1.3), " + prompt

        if negative_prompt:
            self.negative_prompt += negative_prompt
        try:
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/generate/core",
                headers={"authorization": self.api_key, "accept": "application/json"},
                files={"none": ""},
                data={
                    "prompt": request_prompt,
                    "negative_prompt": self.negative_prompt,
                    "output_format": image_format,
                    "aspect_ratio": aspect_ratio,
                },
            )

            response.raise_for_status()
            data = response.json()

            if response.status_code != 200 or data.get("finish_reason") != "SUCCESS":
                raise Exception()

        except RequestException:
            raise

        return data.get("image")
