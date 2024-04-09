from __future__ import annotations

import os
from abc import ABCMeta, abstractmethod
from typing import Callable, Optional, Type, TypeVar

from arsaga_stable_diffusion.prompt.template import StableDiffusionPromptTemplate
from arsaga_stable_diffusion.schemas.types import generator_type, image_format

T = TypeVar("T", bound="BaseImageGenerator")


class BaseImageGenerator(metaclass=ABCMeta):
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

    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        aspect_ratio: Optional[str] = "1:1",
        image_format: image_format = "webp",
        art_style: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        **kwargs,
    ) -> bytes:
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
