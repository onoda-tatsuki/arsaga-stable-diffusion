from __future__ import annotations

from typing import Optional

import requests
from requests.exceptions import RequestException

from arsaga_stable_diffusion.errors.error_message import ErrorMessage
from arsaga_stable_diffusion.errors.exceptions import APIException
from arsaga_stable_diffusion.schemas.types import image_aspect, image_format
from arsaga_stable_diffusion.stable_diffusion.base import (
    BaseImageGenerator,
    ImageGeneratorFactory,
)


@ImageGeneratorFactory.register("v2")
class V2ImageGenerator(BaseImageGenerator):
    def __init__(
        self,
        api_key: Optional[str] = None,
        quality_prompt: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(api_key, quality_prompt, negative_prompt, **kwargs)

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

        try:
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/generate/core",
                headers={"authorization": self.api_key, "accept": "application/json"},
                files={"none": ""},
                data={
                    "prompt": request_prompt,
                    "negative_prompt": (
                        self.negative_prompt + negative_prompt
                        if negative_prompt
                        else self.negative_prompt
                    ),
                    "output_format": image_format,
                    "aspect_ratio": aspect_ratio,
                },
            )

            response.raise_for_status()
            data = response.json()

            if response.status_code != 200 or data.get("finish_reason") != "SUCCESS":
                raise APIException(
                    error=ErrorMessage.STABLE_DIFFUSION_GENERATE_FAILED,
                    status_code=response.status_code,
                    content=data.get("errors")[0],
                )

        except RequestException as err:
            status_code = None
            content = None

            if response := err.response:
                status_code = response.status_code
                content = response.content

            raise APIException(
                error=ErrorMessage.STABLE_DIFFUSION_GENERATE_FAILED,
                status_code=status_code or 500,
                content=content,
            )

        return data.get("image")
