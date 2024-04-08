from __future__ import annotations

import base64
import io
import os
from abc import ABCMeta, abstractmethod
from typing import Optional

import numpy as np

from PIL import Image
from prompt.template import StableDiffusionPromptTemplate


class BaseImageGenerator(metaclass=ABCMeta):
    # todo pydanticで型定義した値を受け取るように修正する?
    def __init__(
        self,
        api_key: Optional[str] = None,
        quality_prompt: str = StableDiffusionPromptTemplate.QUALITY_PROMPT,
        negative_prompt: str = StableDiffusionPromptTemplate.NEGATIVE_PROMPT,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("STABILITY_AI_API_KEY")

        if api_key is None:
            raise ValueError("Missing Stability AI API Key")

        self.api_key = api_key
        self.quality_prompt = quality_prompt
        self.negative_prompt = negative_prompt

    def _decoded_image(self, encoded_data: bytes | str):
        decoded_image = base64.b64decode(encoded_data)
        io_image = Image.open(io.BytesIO(decoded_image))
        image_np = np.array(io_image)

        return decoded_image, image_np

    @abstractmethod
    def generate_image(self, prompt: str, *args, **kwargs):
        pass
