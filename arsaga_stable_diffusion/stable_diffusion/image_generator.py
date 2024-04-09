from __future__ import annotations

import base64
import io
from typing import Optional

import numpy as np
import requests
from PIL import Image
from schemas.types import image_format
from stable_diffusion.base import BaseImageGenerator, ImageGeneratorFactory


@ImageGeneratorFactory.register("v2")
class V2ImageGenerator(BaseImageGenerator):
    def __init__(self):
        super().__init__()

    def generate_image(
        self,
        prompt: str,
        aspect_ratio: Optional[str] = "1:1",
        art_style: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        image_format: image_format = "webp",
    ):
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

        data = response.json()

        if response.status_code == 200 and data.get("finish_reason") == "SUCCESS":
            decoded_image, image_np = self._decoded_image(data.get("image"))

            decoded_image = base64.b64decode(data.get("image"))
            io_image = Image.open(io.BytesIO(decoded_image))
            image_np = np.array(io_image)

        else:
            # todo 返すエラーの型定義の作成
            raise Exception(str(response.json()))

        return image_np
