from typing import Literal, Union

gpt_type = Literal["gpt-4", "gpt-3.5-turbo"]

generator_type = Literal["v2"]

image_format = Literal["jpeg", "png", "webp"]

encoded_bytes = Union[bytes, str]
