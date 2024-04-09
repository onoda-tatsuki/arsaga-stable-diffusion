from __future__ import annotations

import base64
import io
import os
from abc import ABCMeta, abstractmethod
from typing import Callable, Literal, Optional, Type, TypeVar

import numpy as np
from PIL import Image
from prompt.template import StableDiffusionPromptTemplate

# クラスとして定義しても良いが、型ヒントが効かないのでリテラルで宣言している
generator_type = Literal["v2"]

image_format = Literal["jpeg", "png", "webp"]

T = TypeVar("T", bound="BaseImageGenerator")


class BaseImageGenerator(metaclass=ABCMeta):
    # todo pydanticで型定義した値を受け取るように修正する?
    def __init__(
        self,
        api_key: Optional[str] = None,
        quality_prompt: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        **kwargs,
    ) -> None:

        self.api_key = (
            api_key or kwargs.get("api_key") or os.getenv("STABILITY_AI_API_KEY")
        )
        if self.api_key is None:
            raise ValueError("Missing Stability AI API Key")

        self.quality_prompt = (
            quality_prompt
            or kwargs.get("quality_prompt")
            or StableDiffusionPromptTemplate.QUALITY_PROMPT
        )
        self.negative_prompt = (
            negative_prompt
            or kwargs.get("negative_prompt")
            or StableDiffusionPromptTemplate.NEGATIVE_PROMPT
        )

    def _decoded_image(self, encoded_data: bytes | str):
        decoded_image = base64.b64decode(encoded_data)
        io_image = Image.open(io.BytesIO(decoded_image))
        image_np = np.array(io_image)

        return decoded_image, image_np

    # todo 返す値の定義
    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        aspect_ratio: Optional[str] = "1:1",
        art_style: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        image_format: image_format = "webp",
        **kwargs,
    ):
        pass


class ImageGeneratorFactory:
    _generator_types: dict[generator_type, Type[BaseImageGenerator]] = {}

    @classmethod
    def register(cls, generator_type: generator_type) -> Callable:
        def decorator(cls_: Type[T]) -> Type[T]:
            if not issubclass(cls_, BaseImageGenerator):
                raise TypeError("this object is not BaseImageGenerator class")
            cls._generator_types[generator_type] = cls_
            return cls_

        return decorator

    @classmethod
    def create(
        cls,
        generator_type: generator_type,
        api_key: Optional[str] = None,
        *args,
        **kwargs,
    ) -> BaseImageGenerator:
        generator_cls = cls._generator_types.get(generator_type)
        if generator_cls is None:
            raise ValueError(f"Generator type {generator_type} is not registered")

        return generator_cls(api_key, *args, **kwargs)
